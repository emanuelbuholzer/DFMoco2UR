import asyncio
import logging
from collections import namedtuple
from dfmoco2ur.ur.robot import Robot
from dfmoco2ur.ur.dashboard import Dashboard
from dfmoco2ur.df.server import DFMocoServer
from dfmoco2ur.api.server import APIServer

logger = logging.getLogger(__name__)


def get_handle(config):
    Handle = namedtuple('Handle', ['config', 'robot', 'dashboard'])

    robot = Robot(config)
    dashboard = Dashboard(config)

    return Handle(config, robot, dashboard)


async def run(config):
    handle = get_handle(config)

    dfmoco_server = DFMocoServer(handle)

    api_server = await APIServer(handle).start()
    api_addr = api_server.sockets[0].getsockname()
    logger.info(f"Serving the DFMoco2UR API on {api_addr}")

    async with api_server:
        asyncio.ensure_future(dfmoco_server.run())
        await api_server.serve_forever() 
