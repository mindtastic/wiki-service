from bson import ObjectId
from pymongo import MongoClient
from urllib.parse import quote_plus
from os import getenv
from http import HTTPStatus
import logging as log
from .linkHelper import addLinks, createTitleToIdDict, searchContentForLinks


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

        log.info('Overwriting all existing articles')

        # 1. Delete all existing entries in collection
        self.collection.delete_many({})
        if self.collection.estimated_document_count() > 0:
            return {
                "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                "error": "Could not delete existing articles, so insertion could not be done. Please try again"
            }

        # 2. insert all sent articles
        response = self.collection.insert_many(data)

        # 3. create cross article links
        # fetch all articles from DB and create dict to get the ID by article title
        cursor = self.collection.find({})
        titleToID = createTitleToIdDict(cursor)

        # update all articles where links are intended
        for article in data:

            # get the position of the intended references in the content
            # e.g. [(4, 10), (20, 28)]
            indexesOfReferences = searchContentForLinks(article.get("content"))

            if len(indexesOfReferences) > 0:

                # replace the content with a linkified one
                updatedContent = addLinks(article.get("content"), indexesOfReferences, titleToID)
                article["content"] = updatedContent

                # update changed article in the DB
                currentArticleName = article.get("title").strip().lower()
                currentArticleID = ObjectId(titleToID.get(currentArticleName))
                query = {"_id": currentArticleID}
                newValues = {"$set": {"content": article.get("content")}}
                responseUpdate = self.collection.update_one(query, newValues)
                if responseUpdate.matched_count == 0:
                    return {
                        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                        "error": "Linkified Article could not be updated in DB"
                    }

        return {
            "status_code": HTTPStatus.OK,
            "success": len(response.inserted_ids) == len(data),
            "insertedCount": len(response.inserted_ids)
        }

    def delete(self, articleID):
        log.info('Deleting one article')
        response = self.collection.delete_one({"_id": ObjectId(articleID)})
        output = {"success": response.deleted_count == 1}
        return output

    def searchContent(self, searchString: str):
        log.info('Searching the contents of the articles')

        # converts "Wut ABC" to "Wut.*|ABC"
        regex = searchString.replace(" ", ".*|")

        cursor = self.collection.find({
            "$or": [
                {"title": {'$regex': regex, '$options': 'i'}},
                {"content": {'$regex': regex, '$options': 'i'}}
            ]
        })

        articles = []
        for article in cursor:
            articles.append({
                "id": str(article["_id"]),
                "title": article["title"],
                "content": article["content"]
            })
        output = {"articles": articles}

        return output
