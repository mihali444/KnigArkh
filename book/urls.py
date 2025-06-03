from django.urls import path

from book import views
from book.views import toggle_favorite, create_book_offer, EditBookOffer

app_name = 'book'
urlpatterns = [
    path('new/', create_book_offer, name='new-book-offer'),
    path('<uuid:uuid_post>/', views.ShowBookAnnouncement.as_view(), name='book-offer'),
    path('<uuid:uuid_post>/edit/', EditBookOffer.as_view(), name='edit-book-offer'),
    path('toggle-favorite/', toggle_favorite, name='toggle-favorite'),
]
