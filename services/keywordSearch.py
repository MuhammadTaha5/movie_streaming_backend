import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import get_db
from fuzzywuzzy import fuzz

db = get_db()
movies_col = db["movies"]

def keyword_search(title=None, director=None, cast=None):
    query = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if director:
        query["director"] = {"$regex": director, "$options": "i"}
    if cast:
        query["cast.name"] = {"$regex": cast, "$options": "i"}

    results = list(movies_col.find(query, {"_id": 0}))

    # Apply fuzzy ranking for better results
    if title:
        results.sort(key=lambda x: fuzz.partial_ratio(title.lower(), x.get("title", "").lower()), reverse=True)
    elif director:
        results.sort(key=lambda x: fuzz.partial_ratio(director.lower(), x.get("director", "").lower()), reverse=True)
    elif cast:
        results.sort(
            key=lambda x: max([fuzz.partial_ratio(cast.lower(), c.get("name", "").lower()) for c in x.get("cast", [])]),
            reverse=True
        )

    return results
