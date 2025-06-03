from django.contrib import admin

from book.models import Book, Author, Publisher, Photo

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Photo)
