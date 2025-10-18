import sys, os
from bson import ObjectId
from fastapi import HTTPException  # ✅ Add HTTPException here
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import get_db



db = get_db()
reviews_col = db['reviews']
users_col = db['users']
movies_col = db['movies']


def get_movie_reviews(movie_id: str):
    try:
        movie_obj_id = ObjectId(movie_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid movie ID format")

    # Step 1: Get movie details (basic info)
    movie = movies_col.find_one(
        {'_id': movie_obj_id},
        {'title': 1, 'director': 1, 'release_year': 1, 'genres': 1, 'rating': 1}
    )

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Step 2: Join reviews with user info
    pipeline = [
        {'$match': {'movie_id': movie_obj_id}},
        {'$lookup': {
            'from': 'users',
            'localField': 'user_id',
            'foreignField': '_id',
            'as': 'user_info'
        }},
        {'$unwind': '$user_info'},
        {'$project': {
            '_id': 0,
            'review_id': {'$toString': '$_id'},
            'user_id': {'$toString': '$user_id'},
            'user_name': '$user_info.name',
            'user_email': '$user_info.email',
            'rating': 1,
            'review_text': 1,
            'timestamp': 1
        }},
        {'$sort': {'timestamp': -1}}
    ]

    reviews = list(reviews_col.aggregate(pipeline))

    result = {
        'movie_id': str(movie['_id']),
        'title': movie.get('title'),
        'director': movie.get('director'),
        'release_year': movie.get('release_year'),
        'genres': movie.get('genres'),
        'rating_summary': movie.get('rating'),
        'total_reviews': len(reviews),
        'reviews': reviews
    }

    return result


