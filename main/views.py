from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, TemplateView


# Create your views here.
class MainPageView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {"all_books_section_cards": ["new-book.png", "new-book.png", "new-book.png",
                                                  "new-book.png", "new-book.png", "new-book.png",],
                     "cats": [["adventure.png", "Приключение"], ["detective.png", "Детективы"],
                              ["fantastik.png", "Фантастика"], ["fentesi.png", "Фентези"],
                              ["history_prose.png", "Историческая проза"], ["horror.png", "Ужасы"],
                              ["love_romans.png", "Любовная романтика"], ["mistik.png", "Мистика"],
                              ["poesia.png", "Поэзия"], ["other.png", "Другое"]]}



