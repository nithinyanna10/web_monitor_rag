import json
from sentence_transformers import SentenceTransformer
from chroma_connector import batch_insert

MODEL_NAME = 'all-MiniLM-L6-v2'

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python insert_normalized_to_chroma.py <normalized_json>')
        exit(1)
    input_path = sys.argv[1]
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    model = SentenceTransformer(MODEL_NAME)
    texts = []
    metadatas = []
    for site, content in data.items():
        if site == 'site1':
            text = f"{content.get('product', '')}. {content.get('description', '')} Features: {', '.join(content.get('features', []))} Review: {content.get('review', '')}"
        elif site == 'site2':
            text = f"{content.get('headline', '')}. {content.get('body', '')} Tags: {content.get('tags', '')}"
        elif site == 'site3':
            text = f"{content.get('city', '')} weather. {content.get('forecast', '')}"
        elif site == 'site4':
            text = f"{content.get('company_and_ticker', '')}. {content.get('analysis', '')}"
        elif site == 'site5':
            text = f"{content.get('event', '')}. {content.get('description', '')} {content.get('meta', '')} Speakers: {', '.join(content.get('speakers', []))}"
        else:
            text = ''
        if text:
            texts.append(text)
            metadatas.append({'site': site})
    if texts:
        embeddings = model.encode(texts).tolist()
        batch_insert(texts, embeddings, metadatas)
        print(f'Inserted {len(texts)} texts and embeddings into ChromaDB.')
    else:
        print('No texts found to embed.') 