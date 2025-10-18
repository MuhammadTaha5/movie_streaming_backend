import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from services.semanticTitleModel import preprocess
from config.db_config import get_db
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast & efficient

db = get_db()
movies_col = db["movies"]

movies = []
embeddings_list = []

for doc in movies_col.find({}, {"title": 1, "embedding": 1,"rating": 1, "watch_count": 1, "_id": 0}):
    if "embedding" in doc and doc["embedding"] is not None:
        movies.append({"title": doc["title"]})
        embeddings_list.append(doc["embedding"])


# Check if embeddings exist
if not embeddings_list:
    raise ValueError("No embeddings found in database. Please generate title embeddings first.")

# Convert embeddings to numpy array (shape: N x D)
embeddings = np.array(embeddings_list, dtype=np.float32)

# -------------------------------
# Semantic Search Function
# -------------------------------
def semantic_search_title(user_query, top_n=10):
    """
    Perform semantic title search using cosine similarity.
    Returns top N most similar movies.
    """
    # Preprocess and encode user query
    query = preprocess(user_query)
    query_embedding = model.encode([query])  # shape: (1, D)

    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]  # shape: (N,)

    # Get indices of top N similar movies
    top_indices = np.argsort(similarities)[::-1][:top_n]

    # Prepare results
    top_movies = []
    for idx in top_indices:
        movie = movies[idx].copy()
        movie["similarity_score"] = float(similarities[idx])
        top_movies.append(movie)

    return top_movies
