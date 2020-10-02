import logging
import dfmoco2ur.api.handlers as handlers
import asyncio


class Multiplexer:

    def __init__(self, handle):
        self.logger = logging.getLogger(__name__)
        self.handle = handle
        self.handlers = {
            'start_freedrive': handlers.start_freedrive,
            'stop_freedrive': handlers.stop_freedrive
        }
    
    async def run(self, reader, writer):
        while True:
            try:            
                data = await reader.readline()
                self.logger.debug(f"Received message from API: {data}")

                msg = data.decode(encoding='ascii').rstrip().split(' ')
                msg_kind = msg[0]
                msg_args = msg[1:]
                
                # TODO: on exit
                handler = self.handlers.get(msg_kind, False)
                if not handler:
                    self.logger.error(f"Received unknown API message: {data}")
                    continue
                
                res = await handler(self.handle, msg_args)
                msg = f"{res}\n"
                self.logger.debug(f"Sending message to API consumer: {msg}")
                writer.write(bytes(msg, encoding='ascii'))
                await writer.drain()
            except asyncio.IncompleteReadError:
                self.logger.error(f"An incomplete read occured on the DFMocoServer, connection probably lost.")
                break