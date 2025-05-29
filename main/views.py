from django.views.generic import TemplateView

from category.models import Category
from main.models import BookOffer, MainPageList


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

        # Get popular book from MainPageList
        popular_book = MainPageList.objects.filter(type=MainPageList.BookType.POPULAR).select_related(
            'book_offer__book__author'
        ).first()
        context['popular_book'] = popular_book.book_offer if popular_book else None

        # Get new book from MainPageList
        new_book = MainPageList.objects.filter(type=MainPageList.BookType.NEW).select_related(
            'book_offer__book__author'
        ).first()
        context['new_book'] = new_book.book_offer if new_book else None

        return context
