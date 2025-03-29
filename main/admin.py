from django.contrib import admin

from .models import MainPageList, BookOffer, Photo

# Register your models here.
admin.site.register(MainPageList)
admin.site.register(BookOffer)
admin.site.register(Photo)
