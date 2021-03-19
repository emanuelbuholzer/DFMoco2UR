import asyncio
import logging
from dfmoco2ur.df import handlers
from dfmoco2ur.df import heartbeat


class Multiplexer:

    def __init__(self, handle):
        self.logger = logging.getLogger(__name__)
        self.handle = handle
        self.handlers = {
            b'hi': handlers.init_robot,
            b'ms': handlers.are_motors_moving,
            b'mm': handlers.move_motor_to_pos,
            b'mp': handlers.get_motor_pos,
            b'sm': handlers.stop_motor,
            b'sa': handlers.stop_motors,
            b'jm': handlers.jog_motor,
            b'im': handlers.inch_motor,
            b'pr': handlers.set_motor_pulse_rate,
            b'zm': handlers.zero_motor_pos,
            b'np': handlers.set_motor_pos,
            b'go': handlers.unsupported_operation  # Go-Motion (Blur)
        }
    
    async def run(self, reader, writer):
        # Run the heartbeat, to inform about the robots position
        asyncio.ensure_future(heartbeat.run(self.handle, writer))
        await self.handle.userlog.info("DragonFrame connected")
        while True:
            try:
                data = await reader.readuntil(separator=b'\r\n')
                self.logger.debug(f"Received message from Dragonframe: {data}")

                msg_len = len(data)
                msg_kind = data[0:2]
                msg_args = data[3:msg_len-2].split(b' ')
                
                handler = self.handlers.get(msg_kind, False)
                if not handler:
                    self.logger.error(f"Received unknown message: {data}")
                    continue
                    
                res = await handler(self.handle, msg_args)
                msg = f"{res}\r\n"
                self.logger.debug(f"Sending message to Dragonframe: {msg}")
                writer.write(bytes(msg, encoding='ascii'))
                await writer.drain()

            except asyncio.IncompleteReadError:
                self.logger.error(f"An incomplete read occured on the DFMocoServer, connection probably lost.")
                await self.handle.userlog.critical("An internal error occured, please restart the application")
                break