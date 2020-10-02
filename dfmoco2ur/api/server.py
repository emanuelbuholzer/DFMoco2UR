import logging
import asyncio

logger = logging.getLogger(__name__)

async def print_handler(reader, writer):
    while True:
        data = await reader.readline()
        logger.debug(f"Received message from API: {data}")

class APIServer:

    def __init__(self, handle):
        self.handle = handle
    
    async def start(self):
        host = self.handle.config.get('api.host')
        port = self.handle.config.get('api.port')
        server = await asyncio.start_server(print_handler, host, port)
        return server
        