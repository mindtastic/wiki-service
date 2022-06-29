from typing import Optional, List
from pydantic import BaseModel, Field, validator

from wiki_service.models.dbmodel import WikiModelMixin, WikiModel

MAX_LENGTH_OF_TITLE = 50
DEFAULT_ENTRIES_LIMIT = 20
DEFAULT_ENTRIES_OFFSET = 0

class WikiEntry(WikiModelMixin, WikiModel):
    title: str
    content: str

    @validator('title')
    # title must be a string with a length of 5-50 characters
    def title_validator(cls, v):
        if len(v) < 3 or len(v) > MAX_LENGTH_OF_TITLE:
            raise ValueError('the title must have a length between 3 and {}'.format(MAX_LENGTH_OF_TITLE))
        return v.title()

    @validator('content')
    def content_validator(cls, v):
        if len(v) < 1:
            raise ValueError('the content must be longer than 0 characters')
        return v

class WikiEntryInResponse(BaseModel):
    entry: WikiEntry

class ListOfWikiEntries(BaseModel):
    entry_count: int
    entries: List[WikiEntryInResponse]

class WikiEntryFilters(BaseModel):
    query: Optional[str] = None
    limit: int = Field(DEFAULT_ENTRIES_LIMIT, ge=1)
    offset: int = Field(DEFAULT_ENTRIES_OFFSET, ge=0)
