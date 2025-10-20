from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from bson import ObjectId
from config.db_config import get_db

# Database connection
db = get_db()
review_col = db["reviews"]

# Pydantic model for a review
class Review(BaseModel):
    user_id: str = Field(..., description="MongoDB ObjectId of the user")
    movie_id: str = Field(..., description="MongoDB ObjectId of the movie")
    rating: float
    review_text: str

# Helper function to validate ObjectId
def validate_objectid(id_str: str):
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {id_str}")
    return ObjectId(id_str)

# Function to add a review
def addReview(review: Review):
    try:
        # Validate and convert string IDs to ObjectId
        user_oid = validate_objectid(review.user_id)
        movie_oid = validate_objectid(review.movie_id)

        review_data = {
            "user_id": user_oid,
            "movie_id": movie_oid,
            "rating": review.rating,
            "review_text": review.review_text,
            "timestamp": datetime.utcnow()
        }

        result = review_col.insert_one(review_data)
        return str(result.inserted_id)

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except HTTPException as e:
        raise e  # Pass through our validation errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
