from django.urls import path

from profile.views import UserLoginView, logout_views, UserRegisterView

app_name = 'profile'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_views, name='logout'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
]
