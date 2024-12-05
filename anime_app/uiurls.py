from django.urls import path
from .views import(home_page, login_view, logout_view, dashboard_view, register_view)

urlpatterns = [
    path('', home_page, name="home_page"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
