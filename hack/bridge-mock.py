import asyncio
import json
import websockets


mock_responses = {
    "SOCKET_MESSAGE_FREEDRIVE_REQUEST_ENABLE": {
            "type": "SOCKET_MESSAGE_FREEDRIVE_RESPONSE_ENABLE",
            "payload": {
                "timeout": 42    
            }
        },
    "SOCKET_MESSAGE_FREEDRIVE_REQUEST_DISABLE": {
            "type": "SOCKET_MESSAGE_FREEDRIVE_RESPONSE_DISABLE" 
        },
    "SOCKET_MESSAGE_UNLOCK_REQUEST": {
            "type": "SOCKET_MESSAGE_UNLOCK_RESPONSE"
        },

    "SOCKET_MESSAGE_SAVE_REQUEST_ENABLE_DIALOG": {
            "type": "SOCKET_MESSAGE_SAVE_RESPONSE_ENABLE_DIALOG",
           
        },
    "SOCKET_MESSAGE_SAVE_REQUEST": {
            "type": "SOCKET_MESSAGE_SAVE_RESPONSE",
            "payload": {
                "positionName": "sarahclaudiameieerhueber", 
            } 
        },
         "LOAD_POSITION_REQUEST": {
            "type": "LOAD_POSITION_RESPONSE",
            "payload": {
                "positionNames": ["PETER", "markus", "trudi geschter", "mario", "emanuel"], 
            } 
        },
    "GOTO_POSITION_REQUEST":{
        "type": "GOTO_POSITION_RESPONSE"
    }

    }


async def run_mock(websocket, path):
    res_dto = mock_responses["LOAD_POSITION_REQUEST"]
    res = json.dumps(res_dto)
        
    await websocket.send(res)
    while True:
        req = await websocket.recv()
        print(f"< {req}")

        req_dto = json.loads(req)
        req_type = req_dto["type"]

        res_dto = mock_responses[req_type]
        res = json.dumps(res_dto)
        
        await websocket.send(res)
        print(f"> {res}")

start_server = websockets.serve(run_mock, "localhost", 10002)
print("Running bridge mock on port 10002\n")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
