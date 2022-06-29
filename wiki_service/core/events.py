from typing import Callable

from fastapi import FastAPI

from loguru import logger

from wiki_service.core.settings import Settings
from wiki_service.db.mongo import connect_to_mongo, close_mongo_connection

def create_startup_handler(app: FastAPI, settings: Settings) -> Callable:
    @logger.catch
    async def startup_handler() -> None:
        await connect_to_mongo(app, settings)
    
    return startup_handler

def create_shutdown_handler(app: FastAPI, settings: Settings) -> Callable:
    @logger.catch
    async def shutdown_handler() -> None:
        await close_mongo_connection(app)

    return shutdown_handler
