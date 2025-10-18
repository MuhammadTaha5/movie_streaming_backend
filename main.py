import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI, Query
from services.keywordSearch import keyword_search
from services.titleSearchSemantic import semantic_search_title
from services.semanticTitleModel import preprocess

app = FastAPI()
@app.get("/")
def home():
    return {"Mesage": "Hello From Main page"}

@app.get("/search")
def search_movies(
    title: str = Query(None),
    director: str = Query(None),
    cast: str = Query(None),
    limit: int = Query(None)
):
    results = keyword_search(title, director, cast, limit)
    return {"results": results}

@app.get("/movies/title/{title}")
def semanticTitleSearch(title: str):
    result = semantic_search_title(title)
    return {"result": result}