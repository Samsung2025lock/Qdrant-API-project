from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import uuid
import os

COLLECTION_NAME = "text_collection"
client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)

# Create collection if not exists
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"size": 128, "distance": "Cosine"},
    )

def store_in_qdrant(text: str, embedding: list):
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={"text": text},
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_qdrant(embedding: list):
    hits = client.search(collection_name=COLLECTION_NAME, query_vector=embedding, limit=1)
    if not hits:
        return None
    return hits[0].payload.get("text")