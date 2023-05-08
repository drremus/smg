from fastapi import APIRouter, status, HTTPException
from google.cloud import bigquery
import codecs, threading
from routers.model import Sentence, SentenceWithCypher
from google.oauth2 import service_account
import os

CODEC = "rot_13"
lock = threading.Lock()
router_sentences = APIRouter(tags=['sentence'])

# on local docker-compose take the credentials from env variable; on gcloud run it uses the else
key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if key_path:
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
else:
    client = bigquery.Client()


@router_sentences.get(
    "/sentences/{sentenceId}", 
    summary="Get a sentence and its encrypted version",
    description="Get a sentence by Id and the rot13 encryption of it",
    responses={ 200: {"description": "successful operation"},
                404: {"description": "Sentence not found"}},
    response_model=SentenceWithCypher
)
async def get_sentence_by_id(sentenceId: int) -> SentenceWithCypher:
    query = f"select text from sentences.sentences where id = {sentenceId}"
    query_job = client.query(query)
    rows = query_job.result()
    if rows.total_rows:
        row = next(rows)
        return SentenceWithCypher(
            id=sentenceId, text=row.text, cyphered_text=codecs.encode(row.text, CODEC)
        )
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Sentence not found")


@router_sentences.post(
    "/sentences/{Sentence}",
    summary="Add a new sentence to the store",
    description="Add a new sentence to the store",
    responses={ 200: {"description": "successful operation"},
                405: {"description": "Invalid input"}},
    response_model=SentenceWithCypher
)
async def insert_sentence(sentence: Sentence) -> SentenceWithCypher:
    global lock
    with lock:
        query = f"select count(*) as cnt from sentences.sentences where id = {sentence.id}"
        query_job = client.query(query)
        id_exists = next(query_job.result()).cnt
        if id_exists:
            raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail="Invalid input. ID exists!")
        else:
            row_to_insert = [{"id": sentence.id, "text": sentence.text}]
            errors = client.insert_rows_json("sentences.sentences", row_to_insert)
            if not errors:
                return SentenceWithCypher(
                    id=sentence.id,
                    text=sentence.text,
                    cyphered_text=codecs.encode(sentence.text, CODEC),
                )
            else:
                raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail="Invalid input")


# additional endpoint in case a 400 response is needed for non-numeric sentenceId inputs (with sentenceId of type string)
@router_sentences.get(
    "/sentences_id_string/{sentenceId}",
    response_model=SentenceWithCypher,
    responses={ 200: {"description": "successful operation"},
                400: {"description": "Invalid ID supplied, please provide an interer"},
                404: {"description": "Sentence not found"}},
)
async def get_sentence_by_id_sting(sentenceId: str) -> SentenceWithCypher:
    if not sentenceId.isdigit():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid ID supplied, please provide an interer.")

    sentenceId = int(sentenceId)
    query = f"select text from sentences.sentences where id = {sentenceId}"
    query_job = client.query(query)
    rows = query_job.result()
    if rows.total_rows:
        row = next(rows)
        return SentenceWithCypher(
            id=sentenceId, text=row.text, cyphered_text=codecs.encode(row.text, CODEC)
        )
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Sentence not found")
