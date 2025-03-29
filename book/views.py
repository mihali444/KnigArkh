from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from main.models import BookOffer


# Create your views here.
class ShowBookAnnouncement(DetailView):
    template_name = 'book/advertisement.html'
    model = BookOffer
    context_object_name = 'book'

    def get_object(self, **kwargs):
        return get_object_or_404(BookOffer, uuid_post=self.kwargs['uuid_post'], is_published=True)
