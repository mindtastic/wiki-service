from urllib.parse import quote_plus

from bson import ObjectId
from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
from http import HTTPStatus

app = Flask(__name__)


class MongoAPI:
    def __init__(self, ):
        # sets up database client
        uri = "mongodb://%s:%s@%s" % (quote_plus("admin"), quote_plus("test123"), "mymongo_wiki")
        self.client = MongoClient(uri)
        database = "mindtasticWiki"
        collection = "articles"
        db = self.client[database]
        # creates collection in wiki database
        if collection not in db.list_collection_names():
            db.create_collection(collection)
        self.collection = db[collection]

    def read(self):
        log.info('Reading all articles')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing one article')
        response = self.collection.insert_one({"title": data["title"], "content": data["content"]})
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def delete(self, articleID):
        log.info('Deleting one article')
        response = self.collection.delete_one({"_id": ObjectId(articleID)})
        output = {'DeletedCount': str(response.deleted_count)}
        output["success"] = response.deleted_count == 1
        return output


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki', methods=['GET'])
def wiki_readAllArticles():
    db = MongoAPI()
    response = db.read()
    return Response(response=json.dumps(response),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki', methods=['POST'])
def wiki_createArticle():
    data = request.json
    # expects "title" and "content" field in body
    if 'title' not in data or 'content' not in data:
        return Response(response=json.dumps({"Error": "Please provide article information (title and content)"}),
                        status=HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')
    db = MongoAPI()
    response = db.write(data)
    return Response(response=json.dumps(response),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki/<articleID>', methods=['DELETE'])
def wiki_deleteArticle(articleID):
    obj1 = MongoAPI()
    response = obj1.delete(articleID)
    return Response(response=json.dumps(response),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
