from django.views.generic import TemplateView

from main.models import Category


# Create your views here.
class MainPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['all_books'] = ["new-book.png", "new-book.png", "new-book.png",
                                                  "new-book.png", "new-book.png", "new-book.png",]
        return context



