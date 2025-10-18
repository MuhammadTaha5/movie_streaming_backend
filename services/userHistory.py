import sys, os
from bson import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.db_config import get_db
from fastapi import FastAPI

app = FastAPI()

db = get_db()

watchHistory = db['watchHistory']
users = db['users']
movies_col = db['movies']
# def getUserHistoryById(userId):
    
#     user_id = ObjectId(userId)
#     userDetails = users.find_one(
#         {
#             '_id': user_id
#         },
#         {
#             'name': 1,
#             'email': 1,
#             'subscription_type': 1
#         }
#     )
#     history = list(watchHistory.find(
#         {
#             'user_id': user_id
#         }, 
#         {
#             'movie_id': 1,
#             'timestamp': 1,
#             'watch_duration': 1,

#         }
#         ))
    

#     movies = []
#     for h in history:
#         h['_id'] = str(h['_id'])
#         h['movie_id'] = str(h['movie_id'])
#         movie_detail = movies_col.find_one(
#             {
#                 '_id': ObjectId(h['movie_id']),
#             }
#             ,
#             {
#                 'title': 1,
#                 'director': 1,
#                 'popularity': 1
#             }
#         )

#         movie_data = {
#         'title': movie_detail['title'],
#         'director': movie_detail['director'],
#         'popularity': movie_detail['popularity'],
#         'timestamp': h['timestamp'],
#         'watch_duration': h['watch_duration']
#         }
#         movies.append(movie_data)

#     data = {
#         'user_id':str(user_id),
#         'name': userDetails['name'],
#         'email': userDetails['email'],
#         'subscription_type': userDetails['subscription_type'],
#         'movies_watched': movies
#         }
#     return data


def getUserHistoryById(userId):
    user_id = ObjectId(userId)

    userDetails = users.find_one(
        {'_id': user_id},
        {'name': 1, 'email': 1, 'subscription_type': 1}
    )

    pipeline = [
        {'$match': {'user_id': user_id}},
        {'$lookup': {
            'from': 'movies',
            'localField': 'movie_id',
            'foreignField': '_id',
            'as': 'movie_info'
        }},
        {'$unwind': '$movie_info'},
        {'$project': {
            '_id': 0,
            'timestamp': 1,
            'watch_duration': 1,
            'title': '$movie_info.title',
            'director': '$movie_info.director',
            'popularity': '$movie_info.popularity'
        }}
    ]

    movies = list(watchHistory.aggregate(pipeline))

    data = {
        'user_id': str(user_id),
        'name': userDetails['name'],
        'email': userDetails['email'],
        'subscription_type': userDetails['subscription_type'],
        'movies_watched': movies
    }
    return data



@app.get('/users/{userId}/history')
def userHistory(userId: str):
    result = getUserHistoryById(userId)
    return {
        'result': result
    }