from django import template
from django.db.models import QuerySet

from main.models import BookOffer
from user.models import Favorite, User

register = template.Library()


@register.simple_tag(name='check_favorite')
def check_favorite(user: User, offer: BookOffer):
    if not user.is_authenticated:
        return False

    return any(favorite.user == user for favorite in offer.favorite_set.all())
