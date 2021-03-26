import asyncio
import logging

logger = logging.getLogger(__name__)

async def run(handle, writer):
    """
    Inform Dragonframe about the robots position continuously.
    """
    try:
        # Wait until the robot has been setup, before accessing it.
        while not handle.robot.has_setup:
            await asyncio.sleep(1)
        await asyncio.sleep(2)

        heartbeat_interval = handle.config.get('heartbeat.interval')
        while True:
            pos = handle.robot.get_pos()
            for i, p in enumerate(pos):
                message = f"mp {i+1} {p}\r\n"
                writer.write(bytes(message, encoding='ascii'))
                await writer.drain()
            await asyncio.sleep(heartbeat_interval)
    except ConnectionResetError as err:
        # This normally happens, when we disconnect Dragonframe so it's fine
        logger.info("Stopped robot position heartbeat because the connection was reset")