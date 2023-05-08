from fastapi import FastAPI
from routers import sentences
from fastapi.testclient import TestClient

app = FastAPI()
app.include_router(sentences.router_sentences)
client = TestClient(app)


#Tests for GET /sentences/{SentenceID}
def test_get_sentence_by_id_1():
    response = client.get("/sentences/1")
    assert response.status_code == 200
    assert response.json() == {"id":1,"text":"Texas","cyphered_text":"Grknf"}

def test_get_sentence_by_id_1d():
    response = client.get("/sentences/1d")
    assert response.status_code == 422
    assert response.json() == {"detail":[{"loc":["path","sentenceId"],"msg":"value is not a valid integer","type":"type_error.integer"}]}

def test_get_sentence_by_id_1000000000():
    response = client.get("/sentences/100000000")
    assert response.status_code == 404
    assert response.json() == {"detail":"Sentence not found"}


# Tests for GET /sentences_id_string/{SentenceID}
def test_get_sentence_by_id_string_1():
    response = client.get("/sentences_id_string/1")
    assert response.status_code == 200
    assert response.json() == {"id":1,"text":"Texas","cyphered_text":"Grknf"}

def test_get_sentence_by_id_string_1d():
    response = client.get("/sentences_id_string/1d")
    assert response.status_code == 400
    assert response.json() == {"detail":"Invalid ID supplied"}

def test_get_sentence_by_id_string_1000000000():
    response = client.get("/sentences_id_string/100000000")
    assert response.status_code == 404
    assert response.json() == {"detail":"Sentence not found"}


# Tests for POST /sentences/{Sentence}
def test_post_big_integer():
    from datetime import datetime

    bigint = int(datetime.now().timestamp() * 100)
    json = {"id": bigint, "text": "super movie title"}
    response = client.post(url="/sentences/{Sentence}", json=json)
    assert response.status_code == 200
    assert response.json() == {"id": bigint,  "text": "super movie title",  "cyphered_text": "fhcre zbivr gvgyr"}

def test_post_existing_integer():
    json = {"id": 1, "text": "super movie title"}
    response = client.post(url="/sentences/{Sentence}", json=json)
    assert response.status_code == 405
    assert response.json() == {"detail": "Invalid input. ID exists!"}

def test_post_invalid_input():
    json = {"id": "1d", "text": "test"}
    response = client.post(url="/sentences/{Sentence}", json=json)
    assert response.status_code == 422
