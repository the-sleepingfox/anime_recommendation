from django.contrib import admin
from django.urls import path, include
from anime_app.views import home_page

urlpatterns = [
    path('', home_page, name= "home_page" ),
    path('admin/', admin.site.urls),
    path('api/', include('anime_app.urls')),
]