from django.contrib import admin
from django.urls import path, include
from anime_app.views import home_page

urlpatterns = [
    path('', include('anime_app.uiurls') ),
    path('admin/', admin.site.urls),
    path('api/', include('anime_app.urls')),
]