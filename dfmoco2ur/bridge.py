import asyncio
import logging
from collections import namedtuple

from dfmoco2ur import message_handlers
from dfmoco2ur.robot import Robot

_message_handlers = {
    b'hi': message_handlers.init_robot,
    b'ms': message_handlers.are_motors_moving,
    b'mm': message_handlers.move_motor_to_pos,
    b'mp': message_handlers.get_motor_pos,
    b'sm': message_handlers.stop_motor,
    b'sa': message_handlers.stop_motors,
    b'jm': message_handlers.jog_motor,
    b'im': message_handlers.inch_motor,
    b'pr': message_handlers.set_motor_pulse_rate,
    b'zm': message_handlers.zero_motor_pos,
    b'np': message_handlers.set_motor_pos,
    b'go': message_handlers.unsupported_operation  # Go-Motion (Blur)
}


def get_handle(config):
    Handle = namedtuple('Handle', ['robot'])

    robot = Robot(config)

    return Handle(robot)


async def pos_heartbeat(handle, writer):
    pass
    while True:
        for index, pos in enumerate(handle.robot.get_pos()):
            writer.write(bytes(f"mp {index + 1} {pos}\r\n", encoding='ascii'))
            await writer.drain()
        await asyncio.sleep(1)


def get_messsage_handler(_, handle):
    @asyncio.coroutine
    def handle_message(reader, writer):
        pos_heartbeat_task = asyncio.create_task(pos_heartbeat(handle, writer))
        while True:
            try:
                data = yield from reader.readuntil(separator=b'\r\n')
                logging.debug(data)

                # Parse message
                msg_len = len(data)
                msg_kind = data[0:2]
                msg_args = data[3:msg_len-2].split(b' ')
                if msg_kind == b'by':
                    break

                handler = _message_handlers.get(msg_kind, False)
                if not handler:
                    logging.info(f"Received unknown message: {data}")
                    continue

                res = yield from handler(handle, msg_args)

                # TODO: We might want to use multiple outputs
                writer.write(bytes(f"{res}\r\n", encoding='ascii'))
                yield from writer.drain()
            except asyncio.IncompleteReadError as e:
                pass
        yield from pos_heartbeat_task

    return handle_message


async def run(config):
    handle = get_handle(config)

    host = config['df']['host']
    port = config['df']['port']
    message_handler = get_messsage_handler(config, handle)
    server = await asyncio.start_server(message_handler, host, port)

    addr = server.sockets[0].getsockname()
    logging.info(f'Serving DFMoco2UR bridge on {addr}')

    async with server:
        await server.serve_forever()
