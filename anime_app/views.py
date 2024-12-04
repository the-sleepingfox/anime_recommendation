from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserPreference
from .anilist_utils import AnilistClient
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserPreferenceSerializer

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
