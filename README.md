# FastAPI + Qdrant Vector Search API

## Endpoints

### POST /store
```json
{
  "text": "some string to store"
}
```

### POST /retrieve
```json
{
  "query": "substring or related part"
}
```

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```