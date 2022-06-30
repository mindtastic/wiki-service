import os
import sys
import logging
from loguru import logger
from pydantic import BaseSettings
from typing import Tuple

from starlette.datastructures import CommaSeparatedStrings
from wiki_service.core.logging import InterceptHandler
from wiki_service.core.util import MongoConnectionSettings

class Settings(BaseSettings):
    title: str = 'Kopfsachen Wiki'
    debug: bool = False
    allowedHost: CommaSeparatedStrings = CommaSeparatedStrings(os.getenv('ALLOWED_HOSTS', ''))

    api_prefix: str = ''
    mongo_connection: MongoConnectionSettings = MongoConnectionSettings.create_from_environment()

    log_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging.getLogger(logger_name).handlers = [InterceptHandler(level=self.log_level)]
        logger.configure(handlers=[{"sink": sys.stderr, "level": self.log_level}])

    def db_connection_string(self) -> str:
        return self.mongo_connection.connection_string()
