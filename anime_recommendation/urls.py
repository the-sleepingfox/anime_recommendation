from django.contrib import admin
from django.urls import path, include
from anime_app.views import GetRoutes

urlpatterns = [
    path('', GetRoutes.as_view(), name= "get_routes" ),
    path('admin/', admin.site.urls),
    path('api/', include('anime_app.urls')),
]