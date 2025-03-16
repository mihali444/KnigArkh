from django.urls import path

from main.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view()),
]