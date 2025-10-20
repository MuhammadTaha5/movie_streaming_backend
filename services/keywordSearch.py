from config.db_config import get_db
from fuzzywuzzy import fuzz

db = get_db()
movies_col = db["movies"]

def keyword_search(title=None, director=None, cast=None, limit=10):
    """
    Performs fuzzy keyword search across title, director, and cast.
    Returns only the top 'limit' movies sorted by combined match score.
    """
    movies = list(movies_col.find({}, {"_id": 0, "embedding": 0}))
    results = []

    for movie in movies:
        score_details = {"title": 0, "director": 0, "cast": 0}

        # Title fuzzy score
        if title:
            score_details["title"] = fuzz.partial_ratio(title.lower(), movie.get("title", "").lower())

        # Director fuzzy score
        if director:
            dirs = movie.get("director") or movie.get("directors") or []
            if isinstance(dirs, list):
                score_details["director"] = max([fuzz.partial_ratio(director.lower(), d.lower()) for d in dirs])
            else:
                score_details["director"] = fuzz.partial_ratio(director.lower(), dirs.lower())

        # Cast fuzzy score
        if cast and "cast" in movie:
            cast_scores = []
            for c in movie["cast"]:
                name = c.get("name", "") if isinstance(c, dict) else str(c)
                cast_scores.append(fuzz.partial_ratio(cast.lower(), name.lower()))
            score_details["cast"] = max(cast_scores) if cast_scores else 0

        # Combined score
        total_score = score_details["title"] + score_details["director"] + score_details["cast"]
        if total_score > 0:
            movie["match_score"] = total_score
            movie["score_details"] = score_details
            results.append(movie)

    # Sort by match_score descending
    results.sort(key=lambda x: x["match_score"], reverse=True)

    # Return only top 'limit' movies
    return results[:limit]
