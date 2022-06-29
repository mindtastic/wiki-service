from datetime import datetime
from typing import List, Optional
from wiki_service.db.repository import Repository
from wiki_service.db.errors import EntityDoesNotExist
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
        wiki_entry = self.col.find_one({'title': title})
        if wiki_entry is None:
            raise EntityDoesNotExist('WikiEntry with title "{0}" does not exists'.format(title))

        return WikiEntry(**wiki_entry)

    async def create_entry(self, entry: WikiEntry) -> WikiEntry:
        entry_dict = entry.dict()
        entry_dict['updated_at'] = datetime.now()
        created_entry = await self.col.insert_one(entry_dict)

        return WikiEntry(**created_entry)
    