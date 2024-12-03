from django.urls import path
from .views import GetRoutes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', GetRoutes.as_view(), name= 'get_routes'),
    # JWT Authentication Endppoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]