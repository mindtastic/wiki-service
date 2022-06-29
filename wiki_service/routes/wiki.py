from fastapi import APIRouter, Depends
from loguru import logger
from wiki_service.db.entry_repository import EntryRepository


from wiki_service.models.wikiEntry import ListOfWikiEntries, WikiEntry, WikiEntryFilters
from wiki_service.routes.dependencies import _get_db, get_repository, get_wiki_entry_filters


router = APIRouter()

@router.get("", response_model=ListOfWikiEntries)
async def list_wiki_articles(
    filters: WikiEntryFilters = Depends(get_wiki_entry_filters),
    repo: EntryRepository = Depends(get_repository(EntryRepository)),
) -> ListOfWikiEntries:
    logger.debug('Fetching entries with params {}', filters)
    
    entries = await repo.filter_entries(
        seachString=filters.query, 
        limit=filters.limit, 
        offset=filters.offset)   

    return ListOfWikiEntries(entries=entries)