from django.contrib import admin

from .models import MainPageList, BookOffer, Author, Category, Book, Publisher, BookCategory

# Register your models here.
admin.site.register(MainPageList)
admin.site.register(BookOffer)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(BookCategory)

