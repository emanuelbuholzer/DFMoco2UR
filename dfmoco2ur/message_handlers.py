import asyncio
import logging
import numpy as np
from dfmoco2ur import __version__


def unknown_message(_handle, _msg_args):
    logging.error("Received unknown message")
    return ""


def unsupported_operation(_handle, _msg_args):
    logging.info("Unsupported operation called")
    return ""


def init_robot(handle, _msg_args):
    version = __version__
    major_version = __version__.split('.')[0]

    return f"hi {major_version} {handle.robot.num_axes} {version}"


def are_motors_moving(handle, msg_args):
    initial_pos = handle.robot.get_pos()
    max_iters = 5
    for i in range(0, max_iters):
        asyncio.sleep(0.1)
        delta = np.abs(initial_pos - handle.robot.get_pos())
        if delta == np.zeros(6):
            continue
        l_delta = np.logical_and(delta > 0, delta > 0)
        status = ''.join(['1' if d else '0' for d in l_delta])
        return f"ms {status}"
    # After sending a program it might take several 10th of seconds before the robot enters the running state
    return f"ms 000000"


def move_motor_to_pos(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    # TODO: Should we enforce limits?
    pos = msg_args[1]

    pos_delta = pos - handle.robot.get_pos()[axis]
    if pos_delta == 0:
        return f"mp {axis + 1} {pos}"
    else:
        return f"mm {axis + 1} {pos_delta}"


def get_motor_pos(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    pos = handle.robot.get_pos()

    return f"mp {axis + 1} {pos[axis]}"


def stop_motor(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    handle.robot.stop(axis)


def stop_motors(handle, _):
    handle.robot.stop()
    return "sa"


def jog_motor(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    # TODO: Is this really the step pos?
    pos = msg_args[1]
    handle.robot.update_target_pos(axis, pos)
    handle.robot.move_to_target_pos()

    return f"jm {axis - 1}"


def inch_motor(handle, msg_args):
    jog_motor(handle, msg_args)


def set_motor_pulse_rate(handle, msg_args):
    logging.info(f"Tried setting pulse rate, currently not implemented")


def zero_motor_pos(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    handle.robot.zero_motor_pos(axis)


def set_motor_pos(handle, msg_args):
    axis = msg_args[0]
    if msg_args[0] in range(1, handle.robot.num_axes):
        axis -= 1
    else:
        logging.error(f"No such axis ({axis})")
        return ""

    pos = msg_args[1]

    handle.robot.set_motor_pos(axis, pos)
