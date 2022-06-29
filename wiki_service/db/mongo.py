from fastapi import FastAPI
from loguru import logger

from pymongo.errors import AutoReconnect, ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from wiki_service.core.settings import Settings

async def connect_to_mongo(app: FastAPI, settings: Settings):
    logger.info('Connecting to MongoDB...')
    
    try:
        mongo = AsyncIOMotorClient(
            settings.mongo_host, username=settings.mongo_user, password=settings.mongo_password, authMechanism='SCRAM-SHA-256'
        )

        # Send a cheap command to mongo to test availability
        await mongo.admin.command('ismaster')

        app.state.mongo = mongo
        app.state.db = app.state.mongo[settings.mongo_database]
    except (AutoReconnect, ConnectionFailure) as e:
        logger.exception('Error connecting to MongoDB: %s' % e)

    logger.info('Connected to MongoDB.')

async def close_mongo_connection(app: FastAPI):
    logger.info('Closing MongoDB connection...')
    app.state.mongo.close()
    