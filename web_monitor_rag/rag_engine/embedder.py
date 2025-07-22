from sentence_transformers import SentenceTransformer

MODEL_NAME = 'all-MiniLM-L6-v2'
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def embed_text(texts):
    model = get_model()
    if isinstance(texts, str):
        texts = [texts]
    return model.encode(texts).tolist()

if __name__ == '__main__':
    # Test embedding
    print(embed_text(["Hello world!", "Smart RetailOps is cool."]))
