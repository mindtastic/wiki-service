from typing import AsyncGenerator, Callable, Type, Union
from fastapi import Depends, Query
from starlette.requests import Request
from wiki_service.db.repository import Repository
from motor.motor_asyncio import AsyncIOMotorDatabase
from wiki_service.models.wikiEntry import (
    DEFAULT_ENTRIES_LIMIT, 
    DEFAULT_ENTRIES_OFFSET,
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
