from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def compute_embeddings(products):
    model = _get_model()
    texts = [p["norm_title"] for p in products]
    vectors = model.encode(texts)
    for i, p in enumerate(products):
        p["vec"] = vectors[i]
    return products

def similarity(p1, p2):
    return cosine_similarity([p1["vec"]], [p2["vec"]])[0][0]