from django.views.generic import TemplateView

from category.models import Category
from main.models import BookOffer


# Create your views here.
class MainPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['all_books'] = BookOffer.objects.filter(is_published=True).select_related(
            'book__author'
        ).prefetch_related(
            'favorite_set',
        )[:6]
        return context



