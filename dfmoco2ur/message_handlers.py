import asyncio
import logging
import numpy as np
from dfmoco2ur import __version__
from aiolimiter import AsyncLimiter


async def unsupported_operation(_handle, _msg_args):
    logging.info("Unsupported operation called")
    return ""


async def init_robot(handle, _msg_args):
    version = __version__
    major_version = __version__.split('.')[0]

    return f"hi {major_version} {handle.robot.num_axes} {version}"


async def are_motors_moving(handle, msg_args):
    # initial_pos = handle.robot.get_pos()
    # max_iters = 5
    # for i in range(0, max_iters):
    #     await asyncio.sleep(0.1)
    #     delta = np.abs(initial_pos - handle.robot.get_pos())
    #     if (delta == np.zeros(6)).all():
    #         continue
    #     l_delta = np.logical_and(delta > 0, delta > 0)
    #     status = ''.join(['1' if d else '0' for d in l_delta])
    #     return f"ms {status}"
    # # After sending a program it might take several 10th of seconds before the robot enters the running state
    return f"ms 000000"


async def move_motor_to_pos(handle, msg_args):
    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes+1):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    # TODO: Should we enforce limits?
    pos = int(msg_args[1])

    handle.robot.update_target_pos(axis, pos)

    asyncio.ensure_future(handle.robot.move_to_target_pos())

    pos_delta = pos - handle.robot.get_pos()[axis]
    if pos_delta == 0:
        return f"mp {axis + 1} {pos}"
    else:
        return f"mm {axis + 1} {pos_delta}"


async def get_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes+1):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    pos = handle.robot.get_pos()

    return f"mp {axis + 1} {pos[axis]}"


async def stop_motor(handle, msg_args):
    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes+1):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    # handle.robot.stop(axis)

    return f"sm {axis+1}"


async def stop_motors(handle, _):
    handle.robot.stop()
    return "sa"


async def jog_motor(handle, msg_args):
    """
    Move the motor at a reasonable speed into a direction
    """

    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes+1):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    axis_pos = handle.robot.get_pos()[axis]
    jog_factor = handle.config['axis'][axis]['jog_factor']
    relative_goal = np.sign(int(msg_args[1])) * jog_factor

    handle.robot.update_target_pos(axis, axis_pos + relative_goal)
    await handle.robot.move_to_target_pos()

    axis_pos = handle.robot.get_pos()[axis]
    return f"jm {axis + 1}\r\nmp {axis+1} {axis_pos}"


async def inch_motor(handle, msg_args):
    """
    Move the in very small increments into a direction
    """

    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes + 1):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    axis_pos = handle.robot.get_pos()[axis]
    inch_factor = handle.config['axis'][axis]['inch_factor']
    relative_goal = np.sign(int(msg_args[1])) * inch_factor

    handle.robot.update_target_pos(axis, axis_pos + relative_goal)
    await handle.robot.move_to_target_pos()

    axis_pos = handle.robot.get_pos()[axis]
    return f"im {axis + 1}\r\nmp {axis+1} {axis_pos}"


async def set_motor_pulse_rate(handle, msg_args):
    #logging.info(f"Tried setting pulse rate, currently not implemented")
    pass


async def zero_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    handle.robot.zero_motor_pos(axis)


async def set_motor_pos(handle, msg_args):
    axis = int(msg_args[0])
    if axis in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    pos = int(msg_args[1])

    handle.robot.set_motor_pos(axis, pos)
