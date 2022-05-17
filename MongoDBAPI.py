from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
from http import HTTPStatus

app = Flask(__name__)


class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient("mongodb://mymongo_1:27017/")
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        log.info('Reading All Articles')
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Article')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def delete(self, data):
        log.info('Deleting Article')
        response = self.collection.delete_one({"articleID": data["articleID"]})
        output = {'Status': 'Successfully Deleted',
                  'DeletedCount': str(response.deleted_count)}
        return output


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki', methods=['GET'])
def wiki_readAllArticles():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide database name and collection"}),
                        status=HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    return Response(response=json.dumps(response),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki', methods=['POST'])
def wiki_createArticle():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide article information"}),
                        status=HTTPStatus.BAD_REQUEST,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


@app.route('/wiki/<articleID>', methods=['DELETE'])
def wiki_deleteArticle(articleID):
    return Response(response=json.dumps({"Error": "Please provide Wiki Article ID"}),
                    status=HTTPStatus.OK,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

