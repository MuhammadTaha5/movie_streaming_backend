import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timedelta
from bson import ObjectId
from config.db_config import get_db

db = get_db()
watchHistory = db['watchHistory']

# Calculate date 30 days ago
last_month_date = datetime.utcnow() - timedelta(days=30)

pipeline = [
    {
        '$match': {
            'timestamp': {'$gte': last_month_date}  
        }
    },
    {
        '$group': {
            '_id': '$movie_id',
            'total_watches': {'$sum': 1}, 
            'total_watch_time': {'$sum': '$watch_duration'}
        }
    },
    {
        '$sort': {'total_watches': -1}  
    },
    {
        '$limit': 5 
    },
    {
        '$lookup': {
            'from': 'movies',              
            'localField': '_id',
            'foreignField': '_id',
            'as': 'movie_info'
        }
    },
    {
        '$unwind': {
            'path': '$movie_info',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$project': {
            '_id': 0,
            'movie_id': {'$toString': '$_id'},
            'title': '$movie_info.title',
            'total_watches': 1,
            'total_watch_time': 1
        }
    }
]

top_movies = list(watchHistory.aggregate(pipeline))

def getPopularMovies():
    return top_movies