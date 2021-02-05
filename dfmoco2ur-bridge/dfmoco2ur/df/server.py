import logging
import asyncio
from dfmoco2ur.df.multiplexer import Multiplexer


class DFMocoServer:

    def __init__(self, handle):
        self.logger = logging.getLogger(__name__)
        self.handle = handle

    async def start(self):
        host = self.handle.config.get('df.host')
        port = self.handle.config.get('df.port')
        mux = Multiplexer(self.handle)

        server = await asyncio.start_server(mux.run, host, port)
        addr = server.sockets[0].getsockname()
        self.logger.info(f"Serving the DFMoco Server on {addr}")
        return server
