from bson import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
from os import getenv
from http import HTTPStatus
import logging as log


class MongoAPI:
    def __init__(self, ):
        # sets up database client
        user = getenv('MONGODB_USER', "admin")
        password = getenv('MONGODB_PASSWORD', "test123")
        databaseHost = getenv('MONGODB_HOST', "mymongo_wiki")
        uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), databaseHost)
        # THIS IS JUST FOR TESTING PURPOSES
        self.client = MongoClient(uri)
        database = "mindtasticWiki"
        collection = "articles"
        db = self.client[database]
        # creates collection in wiki database
        if collection not in db.list_collection_names():
            db.create_collection(collection)
        self.collection = db[collection]

    def readAll(self):
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

    def readSingle(self, articleID):
        log.info('Reading specific article')
        document = self.collection.find_one(ObjectId(articleID))
        document["_id"] = str(document["_id"])
        document["id"] = document.pop("_id")
        return document

    def write(self, data):
        # this method is supposed to replace all existing
        # entries with the ones coming from the admin service

        # --> admins can just send one json object to this endpoint, which
        # is updated from time to time

        # 1. Delete all existing entries in collection
        self.collection.delete_many({})
        if self.collection.estimated_document_count() > 0:
            return {
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                "error": "Could not delete existing articles, so insertion could not be done. Please try again"
            }

        # 2. insert all send articles
        log.info('Writing many articles')
        response = self.collection.insert_many(data)
        # convert ObjectIDs to strings
        inserted_ids = [str(entry_id) for entry_id in response.inserted_ids]

        return {
            "status_code": HTTPStatus.OK,
            "success": len(inserted_ids) == len(data),
            "document_IDs": inserted_ids
        }

    def delete(self, articleID):
        log.info('Deleting one article')
        response = self.collection.delete_one({"_id": ObjectId(articleID)})
        output = {"success": response.deleted_count == 1, "deletedCount": str(response.deleted_count)}
        return output
