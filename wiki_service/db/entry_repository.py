from datetime import datetime
from typing import List, Optional

from loguru import logger
from wiki_service.db.repository import Repository
from bson.objectid import ObjectId
from wiki_service.db.errors import EntityDoesNotExist, InvalidRequestEntity
from wiki_service.models.wikiEntry import WikiEntry

class EntryRepository(Repository):
    COLLECTION_NAME = 'articles'

    @property
    def collection(self):
        return self.COLLECTION_NAME

    async def filter_entries(
        self, 
        *,
        seachString: Optional[str] = None, 
        limit: int = 20, 
        offset = 0
    ) -> List[WikiEntry]:
        entries: List[WikiEntry] = []
        filter = {}
        if seachString:
            filter["$text"] = {"$search": seachString}

        rows = self.col.find(filter, limit=limit, skip=offset)

        async for row in rows:
            entries.append(WikiEntry(**row))

        return entries

    async def get_entry_by_title(self, title: str) -> WikiEntry:
        wiki_entry = await self.col.find_one({'title': title})
        if wiki_entry is None:
            raise EntityDoesNotExist('WikiEntry with title {} does not exists'.format(title))

        return WikiEntry(**wiki_entry)
    
    async def get_entry_by_id(self, id: str) -> WikiEntry:
        wiki_entry = await self.col.find_one({'_id': ObjectId(id)})
        logger.debug('get_entry_by_id got for id {} entity: {}', id, wiki_entry)
        if wiki_entry is None:
            raise EntityDoesNotExist('WikiEntry with id {} does not exists'.format(id))

        return WikiEntry(**wiki_entry)

    async def create_entry(self, entry: WikiEntry) -> WikiEntry:
        entry_dict = entry.dict()
        entry_dict['updated_at'] = datetime.now()
        db_response = await self.col.insert_one(entry_dict)    

        return entry.copy(update={'id': db_response.inserted_id})

    async def delete_entry(self, entry: WikiEntry) -> None:
        if entry.id is None:
            raise InvalidRequestEntity('Can only delete WikiEntry with id attribute set')

        await self.col.delete_many({'_id': entry.id})