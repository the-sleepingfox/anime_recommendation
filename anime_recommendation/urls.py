from django.contrib import admin
from django.urls import path, include
from anime_app.views import home_page
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('', include('anime_app.uiurls') ),
    path('admin/', admin.site.urls),
    path('api/', include('anime_app.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]