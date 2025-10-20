1️⃣ Project Title & Summary
# 🎬 Movie Streaming Platform Backend

A MongoDB-based backend system for a movie streaming platform that manages movies, users, watch history, and reviews.  
Includes search (keyword, fuzzy, semantic search and hybrid ranking) and analytics using aggregation queries. Also the endpoints to insert, analyze different things.

📘 Overview
## 🧩 Overview
The system provides backend functionality for a movie streaming platform like Netflix.  
It manages movies, users, and user interactions (watch history, reviews), and supports:
- Keyword-based search (title, director, cast)
- Fuzzy matching for typo-tolerant search
- Hybrid ranking based on similarity, rating, and popularity
- Finding average movie rating with numbers of reviews.

⚙️ Features
## ⚙️ Features
- CRUD operations for Movies, Users, and Reviews
- Track user watch history
- Full-text search with typo tolerance(Fuzzy Search to make efficient Searches)
- Hybrid ranking based on similarity, rating, and popularity
- Aggregation-based analytics (e.g., Top 5 most-watched movies)


## 🧠 System Design
The database uses four main collections:

- **movies** → Stores movie information with nested genres and cast.
- **users** → Stores user details and subscription type.
- **watchHistory** → Records user activity (movie watched, timestamp, duration).
- **reviews** → Stores user ratings and text reviews for movies.

**Relationships:**
- One user → many reviews
- One movie → many reviews and watch history entries


## 🗂️ Database Schema
The database uses four main collections:

- **movies** → Stores movie information with nested genres and cast.
{
  "_id": {
    "$oid": "68f25b136fb4862d984a2443"
  },
  "title": "Devil's Acid",
  "description": "Discover reviews, ratings, and trailers for Devil's Acid on Rotten Tomatoes. Stay updated with critic and audience scores today!",
  "release_year": 1933,
  "genres": [
    "Horror"
  ],
  "cast": [
    {
      "name": "Drew Rin Varick"
    },
    {
      "name": "Ashley Dulaney"
    },
    {
      "name": "Jessica Lynn Parsons"
    },
    {
      "name": "Betty Jeune"
    },
    {
      "name": "Eric Gibson"
    }
  ],
  "director": "Garrett Kruithof",
  "rating": {
    "average": 70,
    "review_count": null,
    "ratings_count": 49.33
  },
  "popularity": 0,
  "created_at": "2025-10-17T14:04:59.152542",
  "embedding": not showed here.
}
- **users** → Stores user details and subscription type.
{
  "_id": {
    "$oid": "68f61a544492c966691f91da"
  },
  "name": "Taha",
  "email": "taha.saeed339@gmail.com",
  "subscription_type": "Premium",
  "created_at": {
    "$date": "2025-10-20T11:17:40.990Z"
  }
}

- **watchHistory** → Records user activity (movie watched, timestamp, duration).
{
  "_id": {
    "$oid": "68f26b5d6fb4862d984a24b8"
  },
  "user_id": {
    "$oid": "68f265966fb4862d984a24a0"
  },
  "movie_id": {
    "$oid": "68f25b136fb4862d984a244a"
  },
  "timestamp": {
    "$date": "2025-10-15T17:14:21.901Z"
  },
  "watch_duration": 6931
}
- **reviews** → Stores user ratings and text reviews for movies.
{
  "_id": {
    "$oid": "68f26f366fb4862d984a2534"
  },
  "user_id": {
    "$oid": "68f265966fb4862d984a24a1"
  },
  "movie_id": {
    "$oid": "68f25b136fb4862d984a2457"
  },
  "rating": 7.3,
  "review_text": "Good storyline but a bit slow in the middle.",
  "timestamp": {
    "$date": "2025-09-09T16:30:46.996Z"
  }
}

###  **🌐 API Design**
API endpoints

```markdown
## 🌐 API Design

### 1. GET `/movies/search?query=...`
Searches movies by title, director, or cast with typo tolerance.
Plus it rank by calculating similarity score on Title, director, and cast. It gives final ranking by summation of title, cast, director score.

**Parameters:**
#For Keyword Search
- `query` (string): Search keyword
http://127.0.0.1:8000/search?title=hell&director=smith&cast=tom

First it do regex and then fuzzy search for calculating distance with stored values.
Then it rank accordingly.

**Response Example:**
```json
[
  {
    "title": "The Godfather",
    "rating": 9.2,
    "popularity": 250
  }
]

### 2. GET `/movies/search?query=...`
