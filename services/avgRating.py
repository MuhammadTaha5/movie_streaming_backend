from config.db_config import get_db

from services.reviewsdata import get_movie_reviews

from fastapi import HTTPException

def getAverageRating(movie_id: str):
    # Get full movie review data from your existing function
    ini_result = get_movie_reviews(movie_id)
    
    # Extract title and director
    title = ini_result.get('title', 'N/A')
    director = ini_result.get('director', 'N/A')
    reviews = ini_result.get('reviews', [])
    
    # Calculate average rating safely
    if reviews:
        avg_rating = round(sum([r.get('rating', 0) for r in reviews]) / len(reviews), 2)
        total_reviews = len(reviews)
    else:
        avg_rating = 0
        total_reviews = 0

    # Return clean structured result
    result = {
        "title": title,
        "director": director,
        "average_rating": avg_rating,
        "total_reviews": total_reviews
    }

    return result
