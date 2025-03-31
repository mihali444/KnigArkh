from django import template
from django.db.models import QuerySet

from main.models import BookOffer
from profile.models import Favorite, User

register = template.Library()


@register.simple_tag(name='check_favorite')
def check_favorite(user: User, offer: BookOffer):
    favorites: QuerySet[BookOffer] = user.favorites.all()

    for favorite in favorites:
        if favorite.offer == offer:
            return True

    return False
