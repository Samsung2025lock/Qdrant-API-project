from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.embedding import get_embedding
from app.qdrant_client import store_in_qdrant, search_qdrant

app = FastAPI()

class InputText(BaseModel):
    text: str

class QueryText(BaseModel):
    query: str

@app.post("/store")
def store_text(data: InputText):
    embedding = get_embedding(data.text)
    store_in_qdrant(data.text, embedding)
    return {"message": "Text stored successfully"}

@app.post("/retrieve")
def retrieve_text(query: QueryText):
    embedding = get_embedding(query.query)
    result = search_qdrant(embedding)
    if not result:
        raise HTTPException(status_code=404, detail="No match found")
    return {"matched_text": result}