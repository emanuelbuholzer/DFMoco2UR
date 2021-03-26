import asyncio
import logging
from collections import namedtuple
from dfmoco2ur.ur.robot import Robot
from dfmoco2ur.ur.dashboard import Dashboard
from dfmoco2ur.df.server import DFMocoServer
from dfmoco2ur.api.server import APIServer
from dfmoco2ur.userlog import Logger

logger = logging.getLogger(__name__)


def get_handle(config):
    Handle = namedtuple('Handle', ['config', 'robot', 'dashboard', 'userlog'])

    userlog = Logger(config)
    robot = Robot(config, userlog)
    dashboard = Dashboard(config)    

    return Handle(config, robot, dashboard, userlog)


async def run(config):
    handle = get_handle(config)

    await handle.dashboard.setup()
    await handle.robot.setup(handle.dashboard)

    api_server = await APIServer(handle).start()
    dfmoco_server = await DFMocoServer(handle).start()
    async with dfmoco_server:
        host = handle.config.get('api.host')
        port = handle.config.get('api.port')
        logger.info(f"Serving the DFMoco2UR Websocket API on ws://{host}:{port}")
        asyncio.ensure_future(api_server)
        await dfmoco_server.serve_forever()
