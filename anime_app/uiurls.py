from django.urls import path
from .views import(home_page,
                   login_view,
                   logout_view,
                   dashboard_view,
                   search_view,
                   register_view,
                   preferences_view,
                   recommendations_view
                   )

urlpatterns = [
    path('', home_page, name="home_page"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('search/', search_view, name= 'search'),
    path('preferences/', preferences_view, name= 'preferences'),
    path('recommendations/', recommendations_view, name= 'recommendations')
]
