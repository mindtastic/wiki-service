from typing import List, Optional
from wiki_service.db.repository import Repository

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
