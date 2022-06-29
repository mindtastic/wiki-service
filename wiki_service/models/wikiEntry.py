from pydantic import BaseModel, validator

from wiki_service.models.dbmodel import TimestampsModelMixin, WikiModel

class wikiEntry(TimestampsModelMixin, WikiModel):
    MAX_LENGTH_OF_TITLE = 50

    title: str
    content: str

    @validator('title')
    # title must be a string with a length of 5-50 characters
    def title_validator(cls, v):
        if len(v) < 3 or len(v) > wikiEntry.MAX_LENGTH_OF_TITLE:
            raise ValueError('the title must have a length between 3 and {}'.format(wikiEntry.MAX_LENGTH_OF_TITLE))
        return v.title()

    @validator('content')
    def content_validator(cls, v):
        if len(v) < 1:
            raise ValueError('the content must be longer than 0 characters')
        return v
