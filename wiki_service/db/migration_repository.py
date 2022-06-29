import pymongo
from wiki_service.db.repository import Repository

class MigrationRepository(Repository):

    COLLECTION_NAME = 'wiki_migrations'

    @property
    def collection(self):
        return self.COLLECTION_NAME

    """
    Get all the completed migrations
    """
    async def get_ran(self):
        ran = await self.col.find({},
            sort=[('batch', pymongo.ASCENDING), ('migration', pymongo.ASCENDING)]
        ).to_list(None)

        return list(map(lambda r: r.migration, ran))

    async def migrations_by_batch(self, batch: int):
        return await self.col.find(
            { 'batch': batch },
            sort=[('migration', pymongo.DESCENDING)]
        )

    async def last_batch_number(self):
        last_run = await self.col.find_one({}, sort=[('batch', pymongo.DESCENDING)])
        if last_run is None:
            return 0

        return last_run.batch
    
    async def next_batch_number(self):
        last = await self.last_batch_number()
        return last + 1

    async def log(self, migration: str, batch: int):
        await self.col.insert_one({
            'migration': migration,
            'batch': batch,
        })
