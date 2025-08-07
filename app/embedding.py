import hashlib
import numpy as np

def get_embedding(text: str):
    # Simulated embedding using hash for demo purposes
    hash_object = hashlib.sha256(text.encode())
    hash_digest = hash_object.digest()
    return np.frombuffer(hash_digest[:128], dtype=np.uint8).astype(float).tolist()