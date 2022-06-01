from urllib.parse import quote_plus
from http import HTTPStatus
from bson import ObjectId
from pymongo import MongoClient
from fastapi import FastAPI
import logging as log
from pydantic import ValidationError
from wikiEntry import wikiEntry
from os import getenv

wiki = FastAPI()


class MongoAPI:
    def __init__(self, ):
        # sets up database client
        user = getenv('MONGODB_USER', "admin")
        password = getenv('MONGODB_PASSWORD', "test123")
        databaseName = getenv('MONGODB_NAME', "mymongo_wiki")
        uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), databaseName)
        self.client = MongoClient(uri)
        database = "mindtasticWiki"
        collection = "articles"
        db = self.client[database]
        # creates collection in wiki database
        if collection not in db.list_collection_names():
            db.create_collection(collection)
        self.collection = db[collection]

    def read(self):
        log.info('Reading All Articles')
        documents = self.collection.find()
        articles = []
        for article in documents:
            print(article)
            articles.append({
                "id": str(article["_id"]),
                "title": article["title"],
                "content": article["content"]
            })
        output = {"articles": articles}
        return output

    def write(self, data):
        log.info('Writing one article')
        response = self.collection.insert_one({"title": data["title"],
                                               "content": data["content"]})
        try:
            return {"status": HTTPStatus.OK,
                    "message": "Successfully Inserted",
                    "document_ID": str(response.inserted_id)}
        except AttributeError:
            # if response has no attribute 'inserted_id' (-> insertion failed)
            return {"status": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message": "Insertion failed"}

    def delete(self, articleID):
        log.info('Deleting one article')
        response = self.collection.delete_one({"_id": ObjectId(articleID)})
        output = {"success": response.deleted_count == 1, "deletedCount": str(response.deleted_count)}
        return output


@wiki.get('/')
async def root():
    return {"status": HTTPStatus.OK}


@wiki.get('/wiki')
async def wiki_readAllArticles():
    db = MongoAPI()
    response = db.read()
    response["status"] = HTTPStatus.OK
    return response


@wiki.post('/wiki')
async def wiki_createArticle(entry: wikiEntry):
    print(entry)
    try:
        newWikiEntry = wikiEntry(
            title=entry.title,
            content=entry.content
        )
        db = MongoAPI()
        response = db.write(newWikiEntry.dict())
        return response
    except ValidationError as ve:
        log.info(ve)
        return {"status": HTTPStatus.BAD_REQUEST,
                "error": ve}


@wiki.delete('/wiki/{articleID}')
async def wiki_deleteArticle(articleID):
    db = MongoAPI()
    response = db.delete(articleID)
    response["status"] = HTTPStatus.OK
    return response
