import logging
import asyncio
from dfmoco2ur.api.multiplexer import Multiplexer
import websockets

logger = logging.getLogger(__name__)


class APIServer:

    def __init__(self, handle):
        self.handle = handle
    
    async def start(self):
        host = self.handle.config.get('api.host')
        port = self.handle.config.get('api.port')
        mux = Multiplexer(self.handle)

        start_server = websockets.serve(mux.run, host, port)

        return start_server
        