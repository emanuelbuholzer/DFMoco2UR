import json
import dfmoco2ur.api.actions as actions

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