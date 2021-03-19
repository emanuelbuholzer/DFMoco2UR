import asyncio
import logging
import numpy as np
from dfmoco2ur import __version__
from aiolimiter import AsyncLimiter


logger = logging.getLogger(__name__)
rate_limi = AsyncLimiter(1, 4)


async def unsupported_operation(_handle, _msg_args):
    logger.info("Unsupported operation called")
    return ""


async def init_robot(handle, _msg_args):
    await handle.dashboard.setup()
    await handle.robot.setup(handle.dashboard)

    version = __version__
    major_version = __version__.split('.')[0]
    num_axes = await handle.robot.get_num_axes()
    return f"hi {major_version} {num_axes} {version}"


async def are_motors_moving(handle, msg_args):
    moving = np.array([])

    moving = np.append(moving, handle.robot.is_moving)
    moving = np.append(moving, handle.robot.robot.is_program_running())
    moving = np.append(moving, not handle.robot.at_target)

    if moving.any():
        return "ms 111111"
    else:
        return "ms 000000"



async def move_motor_to_pos(handle, msg_args):
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    # TODO: Should we enforce limits?
    target_pos = int(msg_args[1])

    #await handle.robot.set_target_pos(target_pos, axis)
    asyncio.ensure_future(handle.robot.set_target_pos(target_pos, axis))
    asyncio.ensure_future(handle.robot.move_to_target_pos())

    actual_pos = handle.robot.get_pos()[axis]
    pos_delta = target_pos - actual_pos
    if pos_delta == 0:
        return f"mp {axis + 1} {target_pos}"
    else:
        return f"mm {axis + 1} {pos_delta}"


async def get_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    pos = handle.robot.get_pos()

    return f"mp {axis + 1} {pos[axis]}"


async def stop_motor(handle, msg_args):
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    await handle.robot.stop_axis(axis)

    return f"sm {axis+1}"


async def stop_motors(handle, _):
    handle.robot.stop()
    return "sa"


async def jog_motor(handle, msg_args):
    """
    Move the motor at a reasonable speed into a direction
    """
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    direction = int(msg_args[1])
    await handle.robot.step_axis("jog", axis, direction)

    axis_pos = handle.robot.get_pos()[axis]
    return f"jm {axis + 1}\r\nmp {axis+1} {axis_pos}"


async def inch_motor(handle, msg_args):
    """
    Move the in very small increments into a direction
    """
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    direction = int(msg_args[1])
    await handle.robot.step_axis("inch", axis, direction)

    axis_pos = handle.robot.get_pos()[axis]
    return f"im {axis + 1}\r\nmp {axis+1} {axis_pos}"


async def set_motor_pulse_rate(handle, msg_args):
    return f"pr {msg_args[0]} {msg_args[1]}" 


async def zero_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes+1):
        axis -= 1
    else:
        return ""

    await handle.robot.set_origin_axis(axis)

    return f"zm {axis+1}"


async def set_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    num_axes = await handle.robot.get_num_axes()
    if axis in range(1, num_axes):
        axis -= 1
    else:
        logger.error(f"No such axis ({axis})")
        return ""

    pos = int(msg_args[1])

    await handle.robot.set_origin_axis(axis, pos)

    return f"np {axis+1} {pos}"
