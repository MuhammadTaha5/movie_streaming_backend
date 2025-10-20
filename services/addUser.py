from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from config.db_config import get_db


db = get_db()
user_col = db["users"]


class SubscriptionType(str, Enum):
    premium = "Premium"
    free = "Free"
    standard = "Standard"


class User(BaseModel):
    name: str
    email: str
    subscription_type: SubscriptionType


def addUser(userInfo: User):
    try:
        user_data = {
            "name": userInfo.name,
            "email": userInfo.email,
            "subscription_type": userInfo.subscription_type.value,
            "created_at": datetime.utcnow()
        }
        result = user_col.insert_one(user_data)
        return str(result.inserted_id)
    except PyMongoError as e:
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
