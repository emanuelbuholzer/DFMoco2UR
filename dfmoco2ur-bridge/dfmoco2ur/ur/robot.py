import numpy as np
import urx
import time
import logging
import asyncio
import math3d as m3d
from aiolimiter import AsyncLimiter

from dfmoco2ur.ur.axis.controller import AxisController


class Robot:

    def __init__(self, config):
        self.config = config
        self.lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)
        self.has_setup = False
        self.is_moving = False
        # TODO: This is a FIXME in the original code.
        self.max_float_length = 6

    def _get_pos(self):
        return np.copy(np.array(self.robot.getl()))

    def _speedl(self, velocities, acc):
        """
        Move at given velocities.

        Copied from the python-urx library end removed min_time to make it compatible.
        """
        v = self.robot.csys.orient * m3d.Vector(velocities[:3])
        w = self.robot.csys.orient * m3d.Vector(velocities[3:])
        vels = np.concatenate((v.array, w.array))

        vels = [round(i, self.max_float_length) for i in velocities]
        vels.append(acc)
        prog = "speedl([{},{},{},{},{},{}], a={})".format(*vels)
        self.robot.send_program(prog)

    async def _move_to_target_pos(self):
        pos = None
        await self.lock.acquire()
        try:
            pos = self.axis_controller.unscale_pos(self.target_pos, self._origin)
        finally:
            self.lock.release()
            self.is_moving = True
            self.robot.movel(pos, self.acc, self.vel, wait=True)
            self.at_target = True

    async def _target_within_safety_limits(self):
        async with self.lock:
            pos = self.axis_controller.unscale_pos(self.target_pos, self._origin) 
            pos_rounded = [round(p, self.max_float_length) for p in pos]

            self.robot.set_digital_out(1, False)
            await asyncio.sleep(0.1)

            self.robot.send_program("def myProg():\n  global within_limits= is_within_safety_limits(p[{},{},{},{},{},{}])\n  set_digital_out(1,within_limits)\nend".format(*pos_rounded))
            await asyncio.sleep(0.1)

            return bool(self.robot.get_digital_out(1))

    async def setup(self, dashboard):
        """
        Setup the robot. This method must run before everything else.
        """
        if self.has_setup:
            return

        async with self.lock:
            self.robot = urx.Robot(self.config.get('ur.host'))

        await self.set_tool_center_point(tuple(self.config.get("ur.tool_center_point")))
        await self.set_payload(self.config.get("ur.weight"), tuple(self.config.get("ur.center_of_gravity")))
        await self.set_acc(self.config.get("ur.acc"))
        await self.set_vel(self.config.get("ur.vel"))
        self._free_drive = False
        self.at_target = False
        self.rate_limit = AsyncLimiter(self.config.get("ur.movement_aggregator.max_throughput"), self.config.get("ur.movement_aggregator.interval"))
        self.dashboard = dashboard

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
                self._origin = np.zeros(6)

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
    
    async def set_target_pos(self, target_pos, axis=None):
        """
        Set the target position of the robot on the virtual axis.
        """
        num_axes = await self.get_num_axes()
        if not axis and axis != 0:
            if len(target_pos) != num_axes:
                raise TypeError(f"Target position must be a tuple of length {num_axes}")
            
            async with self.lock:
                self.target_pos = np.copy(np.array(target_pos))
                self.at_target = False
        else:
            if not axis in range(0, num_axes):
                raise Exception(f"No such axis {axis}")
            if not type(target_pos) in [int, np.int, np.int16, np.int32, np.int64]:
                raise TypeError(f"Target position must be an integer {type(target_pos)}")
            
            async with self.lock:
                self.target_pos[axis] = target_pos
                self.at_target = False

    async def move_to_target_pos(self):
        """
        Move the robot to the target position.

        Aggregate movements using a leaky bucket and an initial timeout.
        """
        async with self.rate_limit:
            try:
                await asyncio.sleep(self.config.get("ur.movement_aggregator.initial_timeout"))
                within_limits = await self._target_within_safety_limits()
                if within_limits:
                    await self._move_to_target_pos()
            except urx.urrobot.RobotException:
                self.logger.error("Robot stopped, trying to unlock robot")
                within_limits = await self._target_within_safety_limits()
                if within_limits:
                    await self.dashboard.unlock_protective_stop()
                    await self._move_to_target_pos()
            self.is_moving = False

    async def step_axis(self, kind, axis, direction):
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
        step_acc = self.axis_controller.get_step_acc(kind, axis)

        # TODO: rx, ry, rz don't work soley on their rotation axes, checkout 
        # http://users.cecs.anu.edu.au/~roy/spatial/ for more information
        sv = np.zeros(num_axes).astype(int)
        sv[axis] = normalized_direction
        self.at_target = False
        self._speedl(sv, step_acc)

    async def stop_axis(self, axis):
        """
        Stop the motor moving into a direction.
        """
        num_axes = await self.get_num_axes()
        if not axis in range(0, num_axes):
            raise Exception(f"No such axis {axis}")

        sv = np.zeros(num_axes)
        self._speedl(sv, 0.1)
        pos = self.get_pos()
        await self.set_target_pos(pos)
        self.at_target = True

    def stop(self):
        """
        Stop the robot.
        """
        self.robot.stop()
        self.at_target = True

    async def set_freedrive(self, enabled=True):
        if enabled:
            await self.lock.acquire()
            self.robot.set_freedrive(True, 60*60*24*7)
        else:
            self.robot.set_freedrive(False, 60*60*24*7)
            self.lock.release()