from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Favorite, Subscriber, Reviews

admin.site.register(User, UserAdmin)
admin.site.register(Favorite)
admin.site.register(Subscriber)
admin.site.register(Reviews)
