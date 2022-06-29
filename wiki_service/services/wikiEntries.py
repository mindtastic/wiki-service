from wiki_service.db.errors import EntityDoesNotExist
from wiki_service.db.entry_repository import EntryRepository

async def check_wiki_entry_exists(repo: EntryRepository, title: str) -> bool:
    try:
        await repo.get_entry_by_title(title)
    except EntityDoesNotExist:
        return False
    
    return True
