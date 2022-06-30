from typing import AsyncGenerator, Callable, Type, Union
from fastapi import Depends, HTTPException, Query, Path
from starlette import status
from starlette.requests import Request
from wiki_service.db.entry_repository import EntryRepository
from wiki_service.db.errors import EntityDoesNotExist
from wiki_service.db.repository import Repository
from motor.motor_asyncio import AsyncIOMotorDatabase
from wiki_service.models.wikiEntry import (
    DEFAULT_ENTRIES_LIMIT, 
    DEFAULT_ENTRIES_OFFSET,
    WikiEntry,
    WikiEntryFilters
)

def _get_db(request: Request) -> AsyncIOMotorDatabase:
    return request.app.state.db

def get_repository(repo_type: Type[Repository]) -> Callable[[AsyncIOMotorDatabase], Repository]:
    def _get_repo(db: AsyncIOMotorDatabase = Depends(_get_db)) -> Repository:
        return repo_type(db)
    
    return _get_repo

def get_wiki_entry_filters(
    query: Union[str, None] = None,
    limit: int = Query(DEFAULT_ENTRIES_LIMIT, ge=1),
    offset: int = Query(DEFAULT_ENTRIES_OFFSET, ge=0)
) -> WikiEntryFilters:
    return WikiEntryFilters(
        query=query,
        limit=limit,
        offset=offset
    )

async def get_entry_by_id_from_path(
    id: str = Path(..., min_length=1),
    repo: EntryRepository = Depends(get_repository(EntryRepository))
) -> WikiEntry:
    try:
        return await repo.get_entry_by_id(id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='wiki_entry does not existss'
        )
