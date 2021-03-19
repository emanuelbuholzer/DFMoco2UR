import json
import dfmoco2ur.api.actions as actions
from xdg import XDG_DATA_HOME
import numpy as np
from pathlib import Path


async def enable_freedrive(handle, payload):
    await handle.robot.set_freedrive(True)

    response = {
        "type": actions.SOCKET_MESSAGE_FREEDRIVE_RESPONSE_ENABLE,
        "payload": {
            "timeout": 1000
        }
    }
    return json.dumps(response)


async def disable_freedrive(handle, payload):
    await handle.robot.set_freedrive(False)

    response = {
        "type": actions.SOCKET_MESSAGE_FREEDRIVE_RESPONSE_DISABLE,
    }
    return json.dumps(response)
    
async def unlock(handle, payload):
    await handle.dashboard.unlock_protective_stop()
    await handle.dashboard.close_safety_popup()
    await handle.dashboard.release_brake()

    response = {
        "type": actions.SOCKET_MESSAGE_UNLOCK_RESPONSE
    }
    return json.dumps(response)

async def save_position(handle, payload):
    position_name = payload["positionName"]
    position = handle.robot.get_pos()

    data_dir = Path(XDG_DATA_HOME).joinpath('.dfmoco2ur')
    pos_path = data_dir.joinpath(f"{position_name}.npy")

    with pos_path.open('wb') as p:
        np.save(p,  position)

    response = {
        "type": actions.SOCKET_MESSAGE_SAVE_RESPONSE,
        "payload": {
            "positionName": position_name
        }
    }
    return json.dumps(response)

async def delete_position(handle, payload):
    position_name = payload["positionName"]
    data_dir = Path(XDG_DATA_HOME).joinpath('.dfmoco2ur')
    pos_path = data_dir.joinpath(f"{position_name}.npy")
    pos_path.unlink(missing_ok=True)

    response = {
        "type": actions.DELETE_POSITION_RESPONSE,
        "payload": {
            "positionName": position_name
        }
    }
    return json.dumps(response)

async def goto_position(handle, payload):
    position_name = payload["positionName"]
    data_dir = Path(XDG_DATA_HOME).joinpath('.dfmoco2ur')
    pos_path = data_dir.joinpath(f"{position_name}.npy")
    
    with pos_path.open('rb') as p:
        position = np.load(p)
        
        vel = await handle.robot.get_vel()
        await handle.robot.set_vel(vel*2)
        await handle.robot.set_target_pos(position)
        await handle.robot.move_to_target_pos()
        await handle.robot.set_vel(vel)

        response = {
            "type": actions.GOTO_POSITION_RESPONSE,
            "payload": {
                "positionName": position_name
            }
        }
        return json.dumps(response)