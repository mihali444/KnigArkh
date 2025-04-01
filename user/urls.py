from django.urls import path

from user.views import UserLoginView, logout_views, UserRegisterView, toggle_favorite

app_name = 'profile'

urlpatterns = [
    path('toggle-favorite/', toggle_favorite, name='toggle-favorite'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_views, name='logout'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
]
