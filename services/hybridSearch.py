import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from services.semanticTitleModel import preprocess
from config.db_config import get_db
from sentence_transformers import SentenceTransformer

# -------------------------------
# Load SentenceTransformer model
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')


db = get_db()
movies_col = db["movies"]


movies = []
embeddings_list = []
ratings = []
popularities = []

for doc in movies_col.find({}, {"title": 1, "embedding": 1, "rating": 1, "popularity": 1, "_id": 0}):
    if "embedding" in doc and doc["embedding"] is not None:
        movies.append({
            "title": doc["title"],
            "rating": doc.get("rating", 0.0),
            "popularity": doc.get("popularity", 0)
        })
        embeddings_list.append(doc["embedding"])
        ratings.append(doc.get("rating", 0.0))
        popularities.append(doc.get("popularity", 0))

# Check if embeddings exist
if not embeddings_list:
    raise ValueError("No embeddings found in database. Please generate title embeddings first.")

# Convert to numpy arrays
embeddings = np.array(embeddings_list, dtype=np.float32)
ratings = np.array([m["rating"]["average"] if isinstance(m["rating"], dict) else m["rating"] for m in movies], dtype=np.float32)
popularities = np.array(popularities, dtype=np.float32)

ratings = ratings / 100.0


# Normalize rating and popularity to [0, 1] for fair weighting
def normalize(arr):
    if np.max(arr) == np.min(arr):
        return np.zeros_like(arr)
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

ratings = []
for m in movies:
    if "rating" in m:
        r = m["rating"]
        if isinstance(r, dict) and "average" in r:
            ratings.append(float(r["average"]))
        elif isinstance(r, (int, float)):
            ratings.append(float(r))
        else:
            ratings.append(0.0)
    else:
        ratings.append(0.0)

ratings = np.array(ratings, dtype=np.float32) / 100.0  # normalize 0–1

normalized_ratings = normalize(ratings)
normalized_popularity = normalize(popularities)

# -------------------------------
# Hybrid Semantic Search Function
# -------------------------------
def hybrid_search_title(user_query, top_n=10, w_sim=0.6, w_rating=0.25, w_pop=0.15):
    """
    Hybrid search combining semantic similarity, rating, and popularity.
    """
    # Encode query
    query = preprocess(user_query)
    query_embedding = model.encode([query])  # shape: (1, D)

    # Compute semantic similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]  # shape: (N,)

    # Normalize similarity for fair weighting
    normalized_similarity = normalize(similarities)

    # Compute final hybrid score
    final_scores = (
        w_sim * normalized_similarity +
        w_rating * normalized_ratings +
        w_pop * normalized_popularity
    )

    # Sort movies by final hybrid score
    top_indices = np.argsort(final_scores)[::-1][:top_n]

    # Prepare results
    top_movies = []
    for idx in top_indices:
        movie = movies[idx].copy()
        movie["similarity_score"] = float(similarities[idx])
        movie["final_score"] = float(final_scores[idx])
        top_movies.append(movie)

    return top_movies

print(hybrid_search_title("inception", w_sim=0.7, w_rating=0.2, w_pop=0.1))
