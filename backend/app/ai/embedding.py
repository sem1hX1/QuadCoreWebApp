from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_embeddings(products):
    texts = [p["norm_title"] for p in products]
    vectors = model.encode(texts)

    for i, p in enumerate(products):
        p["vec"] = vectors[i]

    return products

def similarity(p1, p2):
    return cosine_similarity([p1["vec"]], [p2["vec"]])[0][0]