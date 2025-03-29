from django.contrib.auth.views import LoginView
from django.urls import path

from main.views import MainPageView


app_name = 'main'
urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
]