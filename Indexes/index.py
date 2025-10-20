import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import get_db


db = get_db()


movies = db["movies"]

movies.create_index([("title", "text"), ("director", "text"), ("cast.name", "text")],
                    name="movie_text_search",
                    default_language="english")
movies.create_index("release_year")
movies.create_index("genres")
movies.create_index("rating.average")
movies.create_index("popularity")

users = db["users"]

users.create_index("email", unique=True)
users.create_index("name")

reviews = db["reviews"]

reviews.create_index("movie_id")
reviews.create_index("user_id")
reviews.create_index("rating")


watch_history = db["watchHistory"]


watch_history.drop_indexes()


watch_history.create_index("user_id")
watch_history.create_index("movie_id")
watch_history.create_index("timestamp")

print("\nAll indexes recreated successfully!")
