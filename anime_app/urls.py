from django.urls import path
from .views import(
    GetRoutes,
    RegisterView,
    AnimeSearchByNameView,
    AnimeSearchByGenreView,
    UserPreferenceView,
    AnimeRecommendationsView
)

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', GetRoutes.as_view(), name= 'get_routes'),

    # Registering user through my API
    path('auth/register/', RegisterView.as_view(), name='register'),

    # JWT Authentication Endppoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint to search anime
    path('anime/searchbyname/', AnimeSearchByNameView.as_view(), name='anime_search_by_name'),
    path('anime/searchbygenre/', AnimeSearchByGenreView.as_view(), name='anime_search_by_genre'),

    path('user/preferences/', UserPreferenceView.as_view(), name='user_preferences'),
    path('anime/recommendations/', AnimeRecommendationsView.as_view(), name='anime_recommendations'),
]