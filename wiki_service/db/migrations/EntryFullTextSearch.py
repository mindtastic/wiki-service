from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from wiki_service.db.migrations.migration import Migration

class EntryFullTextSearch(Migration):

    def timestamp() -> datetime:
        datetime.isoformat('2022-06-29T12:40:00')

    async def migrate(self, db: AsyncIOMotorDatabase) -> None:
        # Create full text search index
        await db.articles.create_index([
            ('title', 'text'),
            ('content', 'text')
        ])
