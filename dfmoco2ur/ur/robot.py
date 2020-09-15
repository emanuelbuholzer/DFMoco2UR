import numpy as np
import urx
import time
import logging
import asyncio
from aiolimiter import AsyncLimiter

from dfmoco2ur.ur.axis.controller import AxisController


class Robot:

    def __init__(self, config):
        self.config = config
        self.lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        self.has_setup = False

    def _get_pos(self):
        return np.copy(np.array(self.robot.getl()))

    async def setup(self):
        """
        Setup the robot. This method must run before everything else.
        """
        async with self.lock:
            self.robot = urx.Robot(self.config.get('ur.host'))

        await self.set_tool_center_point(tuple(self.config.get("ur.tool_center_point")))
        await self.set_payload(self.config.get("ur.weight"), tuple(self.config.get("ur.center_of_gravity")))
        await self.set_acc(self.config.get("ur.acc"))
        await self.set_vel(self.config.get("ur.vel"))
        self._free_drive = False
        self.rate_limit = AsyncLimiter(self.config.get("ur.movement_aggregator.max_throughput"), self.config.get("ur.movement_aggregator.interval"))

        await self.set_origin()
        async with self.lock:
            self.axis_controller = AxisController(self.config)
            self.axis_controller.set_axis()
            self.target_pos = np.copy(self.axis_controller.scale_pos(self._origin, self._origin))
            self.has_setup = True

    async def set_origin(self, pos = None):
        """
        Set the origin to the given position or use the current position instead.
        """
        if pos:
            self._origin = self.axis_controller.unscale_pos(pos, self._origin)
        else:
            async with self.lock:
                self._origin = self._get_pos()

    async def set_origin_axis(self, axis, pos=None):
        """
        Set an axis origin to zero or pos if given.
        """
        num_axes = await self.get_num_axes()
        if not axis in range(0, num_axes):
            raise Exception(f"No such axis {axis}")
        if pos != None and type(pos) != int:
            raise TypeError("Position must be a signed integer") 
        
        if pos:
            self._origin[axis] = self.axis_controller.unscale_pos(pos, self._origin)[axis]
        else:
            self._origin[axis] = self._get_pos()[axis]


    async def set_acc(self, acc):
        """
        Set the robots acceleration."
        """
        if not type(acc) in [int, float] or acc <= 0:
            raise TypeError("Acceleration must be a number greater then zero.")
        
        async with self.lock:
            self.acc =  acc
        

    async def set_vel(self, vel):
        """
        Set the robots velocity."
        """
        if not type(vel) in [int, float] or vel <= 0:
            raise TypeError("Velocity must be a number greater then zero.")
        
        async with self.lock:
            self.vel = vel
        
    async def set_tool_center_point(self, tcp):
        """
        Set the tool center point in x, y, z, rx, ry, rz.

        For more information on where this point will be, check out the 3D view in the
        initialization screen after changing the values within "Configure TCP".
        """
        if type(tcp) != tuple or len(tcp) != 6:
            raise TypeError("Tool center point must be a tuple of length six: (x, y, z, rx, ry, rz).")            
        
        async with self.lock:
            self.logger.info(f"Setting tool center point {tcp}")
            self.robot.set_tcp(tcp)
            time.sleep(0.2) # Leave some time for the robot to process the setup

    async def set_payload(self, weight, center_of_gravity):
        """
        Set the weight (in kg) and center of gravity relative to the tool center point of the 
        payload being on the tool.
        """
        if not type(weight) in [int, float] or weight < 0:
            raise TypeError("Weight must be a number and must be greater then zero.")
        if type(center_of_gravity) != tuple or len(center_of_gravity) != 3:
            raise TypeError("Center of gravity must be a tuple of length three: (cx, cy, cz)")

        async with self.lock:
            self.logger.info(f"Setting payload weight ({weight}) and center of gravity {center_of_gravity}.")
            self.robot.set_payload(weight=weight, cog=center_of_gravity)
            time.sleep(0.2) # Leave some time for the robot to process the setup

    async def get_num_axes(self):
        """
        Get the number of axes the robot offers for control.
        """
        async with self.lock:
            return self.axis_controller.get_num_axes()

    def get_pos(self):
        """
        Get the robots current position on the virtual axis.
        """
        return self.axis_controller.scale_pos(self._get_pos(), self._origin)
    
    async def set_target_pos(self, axis, target_pos):
        """
        Set the target position of the robot on the virtual axis.
        """
        num_axes = await self.get_num_axes()
        if not axis in range(0, num_axes):
            raise Exception(f"No such axis {axis}")
        if not type(target_pos) in [int, np.int, np.int16, np.int32, np.int64]:
            raise TypeError(f"Target position must be an integer {type(target_pos)}")
        
        async with self.lock:
            self.target_pos[axis] = target_pos
    
    async def _move_to_target_pos(self, wait):
        pos = None
        await self.lock.acquire()
        try:
            pos = self.axis_controller.unscale_pos(self.target_pos, self._origin)
        finally:
            self.lock.release()
            if wait:
                self.robot.movel(pos, self.acc, self.vel, wait=wait)
            else:
                # TODO: Something to combine jogs and inches to make it smoother and faster
                self.robot.movel(pos, self.acc, self.vel, wait=wait)

    async def move_to_target_pos(self, direct=False):
        """
        Move the robot to the target position.

        If direct is true, the robot goes imideately to the destination. Otherwise he tries
        to aggregate movements using a leaky bucket and an initial timeout.
        """
        if direct:
           await self._move_to_target_pos(False)
        else:
            async with self.rate_limit:
                await asyncio.sleep(self.config.get("ur.movement_aggregator.initial_timeout"))
                await self._move_to_target_pos(True)

    async def step(self, kind, axis, direction):
        """
        Move the motor at a reasonable speed into a direction.
        """
        if not kind in ["jog", "inch"]:
            raise TypeError("Step kind must either be jog or inch")
        num_axes = await self.get_num_axes()
        if not axis in range(0, num_axes):
            raise Exception(f"No such axis {axis}")
        if type(direction) != int:
            raise TypeError("Direction must be a signed integer")
        
        normalized_direction = np.sign(direction)
        step_size = self.axis_controller.get_step_size(kind, axis)
        rel_step_goal = normalized_direction * step_size

        axis_pos = self.get_pos()[axis]
        await self.set_target_pos(axis, axis_pos + rel_step_goal)
        await self.move_to_target_pos(direct=True)

    async def stop(self, axis=None):
        if axis == None:
            self.robot.stop()
        elif not axis in range(0, self.get_num_axes()):
            raise TypeError("No such axis {axis}")
        else:
            pos = self.robot.get_pos()
            await self.set_target_pos(axis, pos[axis])
            await self.move_to_target_pos()

    def set_freedrive(self, enabled=True):
        if self._free_drive:
            self.lock.acquire()
            self.robot.set_freedrive(False, 60*60*24*7)
        else:
            self.robot.set_freedrive(True, 60*60*24*7)
            self.lock.release()

    def move_to_origin(self):
        self.robot.movel(self._origin, wait=True)