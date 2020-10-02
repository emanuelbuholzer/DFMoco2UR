import asyncio


class Dashboard:

    def __init__(self, config):
        self.config = config
        self.has_setup = False
        self.unlock_attempts = 0

    async def _read_line(self):
        line = await self.reader.readline()
        return line.decode().rstrip()

    async def _run_command(self, command):
        self.writer.write(f"{command}\n".encode())
        await self.writer.drain()
        res = await self._read_line()
        return res

    async def setup(self):
        """
        Setup the dashboard server client. This must be run before everything else.
        """
        if self.has_setup:
            return

        self.reader, self.writer = await asyncio.open_connection(self.config.get('ur.host'), self.config.get('ur.dashboard_port'))
        res = await self._read_line()
        if res == "Connected: Universal Robots Dashboard Server":
            self.has_setup = True
        else:
            self.has_setup = False
            raise Exception(
                f"Cannot connect to the dashboard server, received: {res}")

    async def close_popup(self):
        """
        Close a popup on the dashboard.
        """
        res = await self._run_command("close popup")
        if res != "closing popup":
            raise Exception(f"Cannot close popup, received: {res}")

    async def power_on(self):
        """
        Power on the robot arm.
        """
        res = await self._run_command("power on")
        if res != "Powering on":
            raise Exception(f"Cannot power on the robot arm, received {res}")

    async def power_off(self):
        """
        Power off the robot arm.
        """
        res = await self._run_command("power off")
        if res != "Powering off":
            raise Exception(f"Cannot power off the robot arm, received {res}")

    async def release_brake(self):
        """
        Release the brakes.
        """
        res = await self._run_command("brake release")
        if res != "Brake releasing":
            raise Exception(f"Cannot release the brakes, received {res}")

    async def unlock_protective_stop(self):
        """
        Unlock the robot arm from a protective stop and close the current popup.
        """
        if self.unlock_attempts >= self.config.get('ur.max_unlock_attempts'):
            raise Exception(f"Cannot unlock robot from protective stop")

        res = await self._run_command("unlock protective stop")
        if res != "Protective stop releasing":
            self.unlock_attempts += 1
            await asyncio.sleep(5)
            await self.unlock_protective_stop()
        self.unlock_attempts = 0

    async def close_safety_popup(self):
        """
        Close a safety popup on the dashboard.
        """
        res = await self._run_command("close safety popup")
        if res != "closing safety popup":
            raise Exception(f"Cannot close safety popup, received {res}")

    async def shutdown(self):
        """
        Shutdown the robot arm.
        """
        res = await self._run_command("shutdown")
        if res != "Shutting down":
            raise Exception(f"Cannot shutdown robot, received {res}")
