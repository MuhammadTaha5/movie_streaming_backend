import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI, Query
from services.keywordSearch import keyword_search
from services.titleSearchSemantic import semantic_search_title
from services.hybridSearch import hybrid_search_title
from services.userHistory import getUserHistoryById
from services.reviewsdata import get_movie_reviews
from services.topWatchedMovies import getPopularMovies
from services.addUser import User, addUser
from services.addReview import Review, addReview
from services.avgRating import getAverageRating


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


@app.get("/movies/hybrid/{title}")
def hybridTitleSearch(title: str):
    result = hybrid_search_title(title)
    return {"message": result}


@app.get('/users/{userId}/history')
def userHistory(userId: str):
    result = getUserHistoryById(userId)
    return {
        'result': result
    }


@app.get("/movies/{movie_id}/reviews")
def movie_reviews(movie_id: str):
    result = get_movie_reviews(movie_id)
    return {'result': result}


@app.get("/topWatchedMovies")
def topWatchedMovies():
    return {
        'Result': getPopularMovies()
    }

@app.post("/users/registration")
def create_user(user: User):
    user_id = addUser(user)
    return {"message": "User added successfully", "user_id": user_id}

@app.post("/Movie/addReview")
def addUserReview(rev: Review):
    reviewId = addReview(rev)
    return {
        'message': 'Review Added successfully', 'review_id': reviewId
    }

@app.get("/movie/{movie_id}/avgRating")
def getAvgRating(movie_id: str):
    return{
        'message': getAverageRating(movie_id)
    }
