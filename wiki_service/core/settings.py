import os
import sys
import logging
from loguru import logger
from pydantic import BaseSettings
from typing import Tuple
from starlette.datastructures import CommaSeparatedStrings

from wiki_service.core.logging import InterceptHandler


class Settings(BaseSettings):
    title: str = 'Kopfsachen Wiki'
    debug: bool = False
    allowedHost: CommaSeparatedStrings = CommaSeparatedStrings(os.getenv('ALLOWED_HOSTS', ''))

    api_prefix: str = ''

    mongo_user: str = os.getenv('MONGODB_USER', "admin")
    mongo_password: str = os.getenv('MONGODB_PASSWORD', '')
    mongo_host: str = os.getenv('MONGODB_HOST', 'mongo_wiki')
    mongo_database: str = os.getenv('MONGODB_DB', 'mindtasticWiki')

    log_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging.getLogger(logger_name).handlers = [InterceptHandler(level=self.log_level)]
        logger.configure(handlers=[{"sink": sys.stderr, "level": self.log_level}])
