async def start_freedrive(handle, args):
    await handle.robot.set_freedrive(True)
    return "start_freedrive"


async def stop_freedrive(handle, args):
    await handle.robot.set_freedrive(False)
    return "stop_freedrive"
    