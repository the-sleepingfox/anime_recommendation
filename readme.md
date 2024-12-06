# **Anime Recommendation System**

This project is an Anime Recommendation System built with Django REST Framework (DRF), AniList GraphQL API, and PostgreSQL. The backend provides REST API endpoints for searching anime, managing user preferences, and fetching recommendations. It also includes JWT-based authentication for secure user interactions.

Deployed at: **[Anime Recommendation System](https://anime-recommendation-i4ri.onrender.com/)**

for testing purpose use 
```arduino
username: testuser
password: password
```
---

## **Features**

- **User Authentication**: Register and login with JWT-based authentication.
- **Anime Search**: Search anime by name or genre using AniList GraphQL API.
- **User Preferences**: Save favorite genres and watched anime.
- **Recommendations**: Get personalized anime recommendations based on user preferences.
- **Database**: Uses PostgreSQL for storing user data and preferences.

---

## **Setup Instructions**

### Prerequisites
- Python 3.8+
- PostgreSQL
- pipenv or virtualenv (optional)

### Steps
1. Clone the repository:
```bash
   git clone https://github.com/your-username/anime-recommendation.git
   cd anime-recommendation
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL:

Create a database (e.g., anime_db).
Configure the database connection in settings.py under DATABASES.

4. Apply migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

6. Access the application locally at:

```arduino
http://127.0.0.1:8000/
```

### API Endpoints

1. Authentication Endpoints
2. 
Endpoint	Method	Description
/auth/register/	POST	Register a new user
/auth/login/	POST	Login and receive a JWT token

2. Register a User
URL: POST https://anime-recommendation-i4ri.onrender.com/auth/register/

Body (JSON):

```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword"
}
```

3. Response:

```json
{
  "message": "User registered successfully"
}
```

4. Login a User
URL: POST https://anime-recommendation-i4ri.onrender.com/auth/login/

Body (JSON):

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
5. Response:

```json
{
  "token": "JWT_TOKEN"
}
```

6. Anime Endpoints

Endpoint	Method	Description
/anime/search/	GET	Search for anime by name or genre
/anime/recommendations/	GET	Get recommendations for the user
Search Anime
URL: GET https://anime-recommendation-i4ri.onrender.com/anime/search/

Query Parameters:

name (optional): Search by anime name.
genre (optional): Search by genre.
Example:

```ruby
GET https://anime-recommendation-i4ri.onrender.com/anime/search/?name=naruto
```

Response:

```json
[
  {
    "id": 12345,
    "title": {
      "romaji": "Naruto",
      "english": "Naruto",
      "native": "ナルト"
    },
    "genres": ["Action", "Adventure"]
  }
]
```

User Preferences Endpoints
Endpoint	Method	Description
/user/preferences/	POST	Save or update user preferences
/user/preferences/	GET	Retrieve user preferences
Save User Preferences
URL: POST https://anime-recommendation-i4ri.onrender.com/user/preferences/
Body (JSON):

```json
{
  "favorite_genres": ["Action", "Comedy"],
  "watched_anime": [12345, 67890]
}
```

Response:

```json
{
  "message": "Preferences updated successfully"
}
```

Get Recommendations
URL: GET https://anime-recommendation-i4ri.onrender.com/anime/recommendations/

Headers:

```json
{
  "Authorization": "Bearer JWT_TOKEN"
}
```
Response:

```json
[
  {
    "id": 54321,
    "title": {
      "romaji": "Attack on Titan",
      "english": "Attack on Titan",
      "native": "進撃の巨人"
    },
    "genres": ["Action", "Drama"]
  }
]
```

Testing with Postman
Import the collection:

Create a new collection in Postman for this API.
Add the base URL: https://anime-recommendation-i4ri.onrender.com/
Test Authentication:

Test /auth/register/ and /auth/login/ endpoints.
Save the JWT token received from /auth/login/.
Test Protected Endpoints:

For /user/preferences/ and /anime/recommendations/, add an Authorization header:

```makefile
Authorization: Bearer JWT_TOKEN
```

Search Anime:

Use the /anime/search/ endpoint with query parameters (name, genre).
Technologies Used
Backend: Django, Django REST Framework
Database: PostgreSQL
API: AniList GraphQL API
Authentication: JWT (via djangorestframework-simplejwt)
Hosting: Render
Contributing
Fork the repository.
Create a new branch: git checkout -b feature-name.
Commit your changes: git commit -m 'Add feature-name'.
Push to the branch: git push origin feature-name.
Submit a pull request.
Feel free to clone, test, and contribute! 😊
>>>>>>> 261386cf13b05c74cf715a6ef4149f013bc4e3dd
