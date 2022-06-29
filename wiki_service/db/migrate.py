from inspect import isclass
from typing import List

from loguru import logger

import wiki_service.db.migrations
from wiki_service.db.migrations import *
from wiki_service.db.migration_repository import MigrationRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

class MongoMigrator:
    MIGRATION_COLLECTION = ''
    
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.repository = MigrationRepository(db)

    async def run(self):
        ran = await self.repository.get_ran()
        pending = self.pending_migrations(ran)

        logger.info('Running migrations ({} pending)', len(pending))

        batch = await self.repository.next_batch_number()
        for migration in pending:
            logger.info('Running migration {}', migration.name)
            await migration.migrate(self.db)
            await self.repository.log(migration.name, batch)

        logger.info('Ran all pending migrations')
    
    def pending_migrations(self, ran: List[str]) -> List[Migration]:
        pending = filter(lambda x: x.name not in ran, self.get_sorted_migrations())
        return list(pending)

    def get_sorted_migrations(self) -> List[Migration]:
        logger.debug('Collecting migrations from module...')


        migrations: List[Migration] = []
        for migration_name in dir(wiki_service.db.migrations):
            attr = getattr(wiki_service.db.migrations, migration_name)

            if isclass(attr) and issubclass(attr, Migration) and not attr.is_abstract():
                migrations.append(attr())

        return sorted(migrations, key=lambda x: x.timestamp)
    
