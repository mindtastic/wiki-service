from fastapi import FastAPI
from loguru import logger

from pymongo.errors import AutoReconnect, ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from wiki_service.core.settings import Settings
from wiki_service.db.migrate import MongoMigrator

async def connect_to_mongo(app: FastAPI, settings: Settings):
    logger.info('Connecting to MongoDB...')
    
    try:
        mongo = AsyncIOMotorClient(
            settings.db_connection_string(),
            authMechanism='SCRAM-SHA-256'
        )

        # Check if articles collection exists
        await mongo.admin.command('ismaster')

        app.state.mongo = mongo
        app.state.db = app.state.mongo[settings.mongo_database]
    except (AutoReconnect, ConnectionFailure) as e:
        logger.exception('Error connecting to MongoDB: %s' % e)

    logger.info('Connected to MongoDB.')

async def close_mongo_connection(app: FastAPI):
    logger.info('Closing MongoDB connection...')
    app.state.mongo.close()

async def migrate_mongo(app: FastAPI):
    migrator = MongoMigrator(app.state.db)
    await migrator.run()
