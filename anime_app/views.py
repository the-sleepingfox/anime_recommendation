from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserPreference
from .anilist_utils import AnilistClient
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserPreferenceSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

def home_page(request):
    return render(request, 'home_page.html')
class GetRoutes(APIView):
    def get(self, request):
        routes = [
            {'GET': 'api/'},
            {'POST': 'api/auth/register/'},
            {'POST': 'api/auth/login/'},
            {'POST': 'api/auth/refresh/'},
            {'GET': 'api/anime/searchbyname/'},
            {'GET': 'api/anime/searchbygenre/'},
            {'GET': 'api/user/preferences'},
            {'PUT': 'api/user/preferences'},
            {'GET': 'api/user/recommendations'},
        ]

        return Response(routes)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully.",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

# View to search anime by name and genre
# http://localhost:8000/api/anime/search/?name=Naruto
class AnimeSearchByNameView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        name= request.query_params.get('name', '')
        data= AnilistClient.anime_search_by_name(name= name)
        return Response(data)

class AnimeSearchByGenreView(APIView):
        def get(self, request):
            genre= request.query_params.get('genre', None)
            data= AnilistClient.anime_search_by_genre(genre= genre)
            return Response(data)
        
class UserPreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Getting the user preferences
        try:
            preferences = UserPreference.objects.get(user=request.user)
            serializer = UserPreferenceSerializer(preferences)
            return Response(serializer.data)
        except UserPreference.DoesNotExist:
            return Response({"error": "Preferences not found for this user."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):

        # Adding or Updating the user's preferences
        try:
            preferences, created = UserPreference.objects.get_or_create(user=request.user)
            serializer = UserPreferenceSerializer(preferences, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AnimeRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'preferences') or not user.preferences.favorite_genres:
            return Response({"error": "Set your preferences first."}, status=status.HTTP_400_BAD_REQUEST)

        recommended_anime = []
        for genre in user.preferences.favorite_genres:
            data = AnilistClient.anime_search_by_genre(genre=genre)
            if "data" in data and "Page" in data["data"]:
                recommended_anime.extend(data["data"]["Page"]["media"])

        return Response(recommended_anime[:10], status=status.HTTP_200_OK)


# views for minimal ui for user interaction

def home_page(request):
    return render(request, 'home_page.html')

# User Registration
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists.'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('/login/')
    return render(request, 'register.html')

# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

# User Logout
def logout_view(request):
    logout(request)
    return redirect('/')

# User Dashboard
@login_required
def dashboard_view(request):
    genres_list= [
            "Action", "Adventure", "Comedy",
            "Drama", "Ecchi", "Fantasy",
            "Hentai","Horror", "Mahou Shoujo",
            "Mecha", "Music", "Mystery",
            "Psychological", "Romance", "Sci-Fi",
            "Slice of Life", "Sports", "Supernatural",
            "Thriller"
            ]
    
    preferences, created= UserPreference.objects.get_or_create(user= request.user)
    
    context= {
        "user_preferences": preferences,
        "genres_list": genres_list
    }
    return render(request, 'dashboard.html', context)

# Anime Search
@login_required
def search_view(request):
    name = request.GET.get('name')
    genre = request.GET.get('genre')
    search_results= []
    if not name and not genre:
        return render(request, 'search_results.html', {'error': 'Please provide a name or genre to search.'})
    elif genre:
        results = AnilistClient.anime_search_by_genre(genre=genre)
        if "data" in results and "Page" in results["data"]:
                search_results.extend(results["data"]["Page"]["media"])
        return render(request, 'search_results.html', {'results': search_results, 'param': genre})
    else:
        results = AnilistClient.anime_search_by_name(name=name)
        print(results)
        print(f"results:  {results['data']['Media']}")
        if "data" in results and "Media" in results["data"]:
            search_results.append(results["data"]["Media"])
            print(f"search: {search_results}")
        return render(request, 'search_results.html', {'results': search_results, 'param':name})


@login_required
def preferences_view(request):
    if request.method == 'POST':
        preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
        favorite_genres = request.POST['favorite_genres'].split(', ')
        watched_anime = request.POST['watched_anime'].split(', ')

        genres_list= [
            "Action", "Adventure", "Comedy",
            "Drama", "Ecchi", "Fantasy",
            "Hentai","Horror", "Mahou Shoujo",
            "Mecha", "Music", "Mystery",
            "Psychological", "Romance", "Sci-Fi",
            "Slice of Life", "Sports", "Supernatural",
            "Thriller"
        ]

        favorite_genres = [genre.title() for genre in favorite_genres if genre.title() in genres_list]
        preferences.favorite_genres = list(set(preferences.favorite_genres + favorite_genres))
        preferences.watched_anime = list(set(preferences.watched_anime + watched_anime))
        preferences.save()


    return redirect('/dashboard/')


@login_required
def recommendations_view(request):
    try:
        # Fetch the user's preferences
        preferences = UserPreference.objects.get(user=request.user)
        favorite_genres = preferences.favorite_genres

        if not favorite_genres:
            return render(request, 'recommendations.html', {'error': 'No favorite genres found in your preferences.'})

        # Fetch recommendations from AniList for each favorite genre
        recommendations = []
        for genre in favorite_genres:
            genre_recommendations = AnilistClient.anime_search_by_genre(genre=genre)

            if "data" in genre_recommendations and "Page" in genre_recommendations["data"]:
                recommendations.extend(genre_recommendations["data"]["Page"]["media"])

        unique_recommendations = {anime['id']: anime for anime in recommendations}
        cleaned_recommendations = list(unique_recommendations.values())
        cleaned_recommendations.sort(key=lambda x: x['popularity'], reverse=True)

        return render(request, 'recommendations.html', {"recommendations": cleaned_recommendations})

    except UserPreference.DoesNotExist:
        return render(request, 'recommendations.html', {'error': 'No preferences found. Please update your preferences.'})
