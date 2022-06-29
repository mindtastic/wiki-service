from typing import List, Optional

from bson import ObjectId
from wiki_service.db.repository import Repository

from wiki_service.models.wikiEntry import WikiEntry

class EntryRepository(Repository):

    @property
    def collection(self):
        return 'articles'

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
            entries.append(WikiEntry(
                **row,
                created_at=ObjectId(row["_id"]).generation_time,
            ))

        return entries
