from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

client = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "texts"

# Ensure collection exists
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

def upsert_to_qdrant(text, vector):
    payload = {"text": text}
    point = PointStruct(id=hash(text), vector=vector, payload=payload)
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def query_qdrant(vector):
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5
    )
    return [r.payload["text"] for r in results]
