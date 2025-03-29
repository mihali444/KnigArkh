from django.urls import path

from book import views


app_name = 'book'
urlpatterns = [
    path('<uuid:uuid_post>/', views.ShowBookAnnouncement.as_view(), name='book-offer'),
]