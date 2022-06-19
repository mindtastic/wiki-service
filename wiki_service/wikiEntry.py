from pydantic import BaseModel, validator
from typing import List
# import datetime


class wikiEntry(BaseModel):
    title: str
    content: List[dict]

    # TODO: add more attributes in future versions
    # date: datetime.date
    # tags: List[str]

    @validator('title')
    # title must be a string with a length of 5-50 characters
    def title_validator(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('the title must have a length between 3 and 50')
        return v.title()

    @validator('content')
    # must be a string with at least 20 characters
    def content_validator(cls, v):
        if len(v) < 1:
            raise ValueError('the content list must be longer than 0')
        for paragraph in v:
            if len(paragraph.get("text")) == 0:
                raise ValueError('the content must have at least 1 character')
        return v

    """
    @validator('date')
    # can't be a date after today
    def date_validator(cls, v):
        if v > datetime.date.today():
            raise ValueError('the publishing date can not be in the future')
        return v

    @validator('tags')
    # all tags must be strings
    def tags_validator(cls, v):
        if not all(isinstance(tag, str) for tag in v):
            raise ValueError('all tags must be strings')
        return v
    """