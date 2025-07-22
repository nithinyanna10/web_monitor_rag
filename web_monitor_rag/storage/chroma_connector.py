import chromadb
import os

CHROMA_COLLECTION = os.getenv('CHROMA_COLLECTION', 'site_embeddings')

client = chromadb.Client()


def get_collection():
    if CHROMA_COLLECTION not in [c.name for c in client.list_collections()]:
        return client.create_collection(CHROMA_COLLECTION)
    return client.get_collection(CHROMA_COLLECTION)

def insert_text(text, embedding, metadata=None):
    col = get_collection()
    col.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata or {}]
    )

def fetch_all():
    col = get_collection()
    return col.get()

if __name__ == '__main__':
    # Example usage
    import numpy as np
    dummy_text = "This is a test sentence."
    dummy_embedding = np.random.rand(768).tolist()  # Example 768-dim embedding
    insert_text(dummy_text, dummy_embedding, {"site": "site1"})
    print(fetch_all())
