from http import HTTPStatus
from typing import Union, List, Dict, Any
import ast
from fastapi import FastAPI
import logging as log
from fastapi.encoders import jsonable_encoder

from .wikiEntry import wikiEntry
from .mongoAPI import MongoAPI

wiki = FastAPI()


@wiki.get('/')
async def root():
    return {"status_code": HTTPStatus.OK}


@wiki.get('/wiki')
async def wiki_readAllArticles():
    db = MongoAPI()
    response = db.readAll()
    response["status_code"] = HTTPStatus.OK
    return response


@wiki.get('/wiki/{articleID}')
async def wiki_readSingleArticle(articleID):
    db = MongoAPI()
    response = db.readSingle(articleID)
    response["status_code"] = HTTPStatus.OK
    return response


@wiki.post('/wiki')
async def wiki_storeArticles(JSONentries: Union[List, Dict, Any] = None):
    entries = ast.literal_eval(jsonable_encoder(JSONentries))

    for entry in entries.get("articles"):
        # validate each entry
        try:
            wikiEntry(
                title=entry.get("title"),
                content=entry.get("content")
            )
        except ValueError as ve:
            log.info(ve)
            return {"status_code": HTTPStatus.BAD_REQUEST,
                    "success": False,
                    "article": "Error in article: {}".format(entry.get("title")),
                    "error": str(ve)}

    db = MongoAPI()
    response = db.write(entries.get("articles"))
    return response


@wiki.delete('/wiki/{articleID}')
async def wiki_deleteArticle(articleID):
    db = MongoAPI()
    response = db.delete(articleID)
    response["status_code"] = HTTPStatus.OK
    return response
