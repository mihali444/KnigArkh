from django.urls import path
from user.views import ProfileView, ProfileEditView, ProfilePasswordChangeView, subscribe

app_name = 'profile'

urlpatterns = [
    path('edit/', ProfileEditView.as_view(), name='edit'),
    path('change-password/', ProfilePasswordChangeView.as_view(), name='change-password'),
    path('subscribe/', subscribe, name='subscribe'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
]
