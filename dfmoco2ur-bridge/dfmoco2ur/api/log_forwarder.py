import json
import dfmoco2ur.api.actions as actions

async def run(handle, websocket):
    while True:
        log_entry = await handle.userlog.get_log()

        response = {
           "type": actions.SOCKET_MESSAGE_LOG,
           "payload": {
               "timestamp": log_entry[0],
               "severity": log_entry[1],
               "message": log_entry[2]
           }
        }
        await websocket.send(json.dumps(response))