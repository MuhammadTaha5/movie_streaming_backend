import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import get_db
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


import re
def preprocess(text):
    return re.sub(r'[^\w\s]', '', text.lower().strip())

db = get_db()
movies_col = db["movies"]

# Load movies and embeddings
movies = list(movies_col.find({}, {"_id": 0, "title": 1, "embedding": 1}))
embeddings_list = [m["embedding"] for m in movies if "embedding" in m]

if len(embeddings_list) == 0:
    raise ValueError("No embeddings found in the database!")

# Convert to 2D numpy array
embeddings = np.array(embeddings_list)  # shape: (num_movies, embedding_dim)

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(user_query, top_n=10):
    query_embedding = model.encode([user_query])  # shape: (1, embedding_dim)
    similarities = cosine_similarity(query_embedding, embeddings)  # shape: (1, num_movies)
    
    top_indices = np.argsort(similarities[0])[::-1][:top_n]
    
    top_movies = []
    for i in top_indices:
        movie = movies[i].copy()
        movie['similarity_score'] = float(similarities[0][i])
        top_movies.append(movie)
    
    return top_movies


