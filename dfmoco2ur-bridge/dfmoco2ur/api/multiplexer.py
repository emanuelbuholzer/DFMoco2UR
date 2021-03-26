import logging
import dfmoco2ur.api.actions as actions
import dfmoco2ur.api.handlers as handlers
import dfmoco2ur.api.log_forwarder as log_forwarder
import dfmoco2ur.api.position_dumper  as position_dumper
import asyncio
import websockets
import json

class Multiplexer:

    def __init__(self, handle):
        self.logger = logging.getLogger(__name__)
        self.handle = handle
        self.handlers = {
            actions.SOCKET_MESSAGE_FREEDRIVE_REQUEST_ENABLE: handlers.enable_freedrive,
            actions.SOCKET_MESSAGE_FREEDRIVE_REQUEST_DISABLE: handlers.disable_freedrive,
            actions.SOCKET_MESSAGE_UNLOCK_REQUEST: handlers.unlock,
            actions.SOCKET_MESSAGE_SAVE_REQUEST: handlers.save_position,
            actions.DELETE_POSITION_REQUEST: handlers.delete_position,
            actions.GOTO_POSITION_REQUEST: handlers.goto_position
        }

    async def run(self, websocket, path):
        # Run the user logging handler continuously
        asyncio.ensure_future(log_forwarder.run(self.handle, websocket))
        await position_dumper.run(websocket)
        while True:
            try:
                data = await websocket.recv()
                self.logger.debug(f"Received message from API: {data}")

                action = json.loads(data)

                action_type = action["type"]
                action_payload = None
                if "payload" in action:
                    action_payload = action["payload"]       

                # TODO: On exit is crazy
                handler = self.handlers.get(action_type, False)
                if not handler:
                    self.logger.error(f"Received unknown API message: {data}")
                    break

                res = await handler(self.handle, action_payload)
                self.logger.debug(f"Sending message to API consumer: {res}")
                await websocket.send(res)
            except websockets.exceptions.ConnectionClosed:
                self.logger.info("API connection closed, probably a refresh.")
                break