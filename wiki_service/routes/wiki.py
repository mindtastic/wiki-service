from http.client import HTTPException
from fastapi import APIRouter, Body, Depends, HTTPException
from loguru import logger

from starlette import status

from wiki_service.db.entry_repository import EntryRepository
from wiki_service.models.wikiEntry import ListOfWikiEntries, WikiEntry, WikiEntryInResponse, WikiEntryFilters
from wiki_service.services.wikiEntries import check_wiki_entry_exists
from wiki_service.routes.dependencies import get_repository, get_wiki_entry_filters


router = APIRouter()

@router.get("", response_model=ListOfWikiEntries,name='wiki:list-entries')
async def list_wiki_articles(
    filters: WikiEntryFilters = Depends(get_wiki_entry_filters),
    repo: EntryRepository = Depends(get_repository(EntryRepository)),
) -> ListOfWikiEntries:
    logger.debug('Fetching entries with params {}', filters)
    
    entries = await repo.filter_entries(
        seachString=filters.query, 
        limit=filters.limit, 
        offset=filters.offset)   

    entries_in_response = [
        WikiEntryInResponse(entry=entry) for entry in entries
    ]

    return ListOfWikiEntries(
        entry_count=len(entries_in_response),
        entries=entries_in_response,
    )

adminRouter = APIRouter()
@adminRouter.post("",status_code=status.HTTP_201_CREATED,name='wiki:create-entry')
async def create_new_article(
    new_entry: WikiEntry = Body(..., embed=True, alias="entry"),
    repo: EntryRepository = Depends(get_repository(EntryRepository))
) -> WikiEntryInResponse:
    if await check_wiki_entry_exists(repo, new_entry.title):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='wiki entry with title {0} already exists'.format(new_entry.title)
        )
    
    entry = await repo.create_entry(new_entry)
    return WikiEntryInResponse(entry=entry)

