import json
from wiki_service.main import wiki
from fastapi.testclient import TestClient
from testData import ARTICLES_VALID, ARTICLES_INVALID_V1, ARTICLES_INVALID_V2

# create test client
test_client = TestClient(wiki)


# inserting articles that will be validated successfully
def test_insertValidArticles():
    response = test_client.post("/wiki", json.dumps(ARTICLES_VALID, default=str))
    assert response.json().get("status_code") == 200
    assert response.json().get("success")
    assert len(response.json().get("document_IDs")) == 2


# inserting articles that will NOT be validated successfully
def test_insertInvalidArticles1():
    response = test_client.post("/wiki", json.dumps(ARTICLES_INVALID_V1, default=str))
    assert response.json().get("status_code") == 400
    assert not response.json().get("success")
    assert response.json().get("article") == "Error in article: T"
    assert response.json().get("error") is not None


# inserting articles that will NOT be validated successfully
def test_insertInvalidArticles2():
    response = test_client.post("/wiki", json.dumps(ARTICLES_INVALID_V2, default=str))
    assert response.json().get("status_code") == 400
    assert not response.json().get("success")
    assert response.json().get("article") == "Error in article: Test 2"
    assert response.json().get("error") is not None


# test root endpoint
def test_root():
    response = test_client.get("/")
    assert response.json().get("status_code") == 200


# test get all articles endpoint
def test_readAllArticles():
    response = test_client.get("/wiki")
    assert response.json().get("status_code") == 200
    assert response.json().get("articles") is not None


# test get articles by id endpoint
def test_readOneArticle():
    responseMany = test_client.get("/wiki")
    article_id = responseMany.json().get("articles")[0].get("id")
    responseSingle = test_client.get("/wiki/{}".format(article_id))
    assert responseSingle.json().get("status_code") == 200
    assert responseSingle.json().get("id") is not None
    assert responseSingle.json().get("title") is not None
    assert responseSingle.json().get("content") is not None


# test delete one article by id endpoint
def test_deleteOneArticle():
    responseMany = test_client.get("/wiki")
    article_id = responseMany.json().get("articles")[0].get("id")
    response = test_client.delete("/wiki/{}".format(article_id))
    assert response.json().get("status_code") == 200
    assert response.json().get("success")
    assert int(response.json().get("deletedCount")) == 1
