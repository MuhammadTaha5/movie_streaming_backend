import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI, Query
from services.keywordSearch import keyword_search

app = FastAPI()
@app.get("/")
def home():
    return {"Mesage": "Hello From Main page"}

@app.get("/search")
def search_movies(
    title: str = Query(None),
    director: str = Query(None),
    cast: str = Query(None)
):
    results = keyword_search(title, director, cast)
    return {"results": results}
