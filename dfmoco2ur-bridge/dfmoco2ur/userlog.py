import asyncio
import logging
import time

class Logger:

    def __init__(self, config):
        self.config = config
        self.internal_logger = logging.getLogger(__name__)
        self.user_log_q = asyncio.Queue()

    def internal_debug(self, message):
        self.internal_logger.debug(message)

    def internal_info(self, message):
        self.internal_logger.info(message)

    def internal_warn(self, message):
        self.internal_logger.warn(message)

    def internal_error(self, message):
        self.internal_logger.error(message)

    def internal_critical(self, message):
        self.internal_logger.critical(message)
    
    async def debug(self, message):
        timestamp = time.time()
        self.internal_logger.debug(f"Logging DEBUG for user: {message}")
        await self.log(timestamp, "DEBUG", message)

    async def info(self, message):
        timestamp = time.time()
        self.internal_logger.info(f"Logging INFO for user: {message}")
        await self.log(timestamp, "INFO", message)

    async def warn(self, message):
        timestamp = time.time()
        self.internal_logger.warn(f"Logging WARN user: {message}")
        await self.log(timestamp, "WARN", message)

    async def error(self, message):
        timestamp = time.time()
        self.internal_logger.error(f"Logging ERROR user: {message}")
        await self.log(timestamp, "ERROR", message)

    async def critical(self, message):
        timestamp = time.time()
        self.internal_logger.critical(f"Logging CRITICAL user: {message}")
        await self.log(timestamp, "CRITICAL", message) 

    async def log(self, timestamp, severity, message):
        return await self.user_log_q.put((timestamp, severity, message))

    async def get_log(self):
        return await self.user_log_q.get()
