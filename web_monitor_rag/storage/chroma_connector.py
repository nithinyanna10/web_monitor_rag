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

def batch_insert(texts, embeddings, metadatas=None, ids=None):
    col = get_collection()
    if ids is None:
        ids = [f"doc_{i}" for i in range(len(texts))]
    col.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas or [{} for _ in texts]
    )

def fetch_all():
    col = get_collection()
    return col.get()

if __name__ == '__main__':
    # Example: Insert normalized data from a JSON file
    import sys
    from sentence_transformers import SentenceTransformer
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python chroma_connector.py <normalized_json>")
        sys.exit(1)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    input_path = sys.argv[1]
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = []
    metadatas = []
    for site, content in data.items():
        # Choose main text fields for embedding
        if site == 'site1':
            text = content.get('description', '')
        elif site == 'site2':
            text = content.get('body', '')
        elif site == 'site3':
            text = content.get('forecast', '')
        elif site == 'site4':
            text = content.get('analysis', '')
        elif site == 'site5':
            text = content.get('description', '')
        else:
            text = ''
        if text:
            texts.append(text)
            metadatas.append({'site': site})
    if texts:
        embeddings = model.encode(texts).tolist()
        ids = [f"{meta['site']}_{i}" for i, meta in enumerate(metadatas)]
        batch_insert(texts, embeddings, metadatas, ids)
        print(f"Inserted {len(texts)} texts and embeddings into ChromaDB.")
    else:
        print("No texts found to embed.")
