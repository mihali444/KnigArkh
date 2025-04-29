from django.urls import path

from book import views
from book.views import toggle_favorite

app_name = 'book'
urlpatterns = [
    path('<uuid:uuid_post>/', views.ShowBookAnnouncement.as_view(), name='book-offer'),
    path('toggle-favorite/', toggle_favorite, name='toggle-favorite'),
]
