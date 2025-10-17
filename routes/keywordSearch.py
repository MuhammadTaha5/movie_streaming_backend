from fastapi import APIRouter, Query
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.keywordSearch import keyword_search


router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/movies")
def search_movies_endpoint(
    title: str | None = Query(None, description="Search by movie title"),
    director: str | None = Query(None, description="Search by director name"),
    cast: str | None = Query(None, description="Search by cast member name")
):
    """
    Fuzzy search movies by title, director, or cast.
    You can pass any combination of parameters.
    Example: /search/movies?title=earth&director=roy
    """
    results = keyword_search(title=title, director=director, cast=cast)
    return {"count": len(results), "results": results}
