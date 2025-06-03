from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from category.models import Category
from main.models import BookOffer, MainPageList
from .forms import BookOfferForm, PhotoFormSet


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


def index(request):
    """
    Представление главной страницы.
    
    Отображает:
    - Популярные объявления
    - Новые объявления
    - Избранные объявления
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Отрендеренная страница с объявлениями
    """
    popular_offers = MainPageList.objects.filter(type='popular').select_related('book_offer', 'book_offer__book', 'book_offer__user')
    new_offers = MainPageList.objects.filter(type='new').select_related('book_offer', 'book_offer__book', 'book_offer__user')
    featured_offers = MainPageList.objects.filter(type='featured').select_related('book_offer', 'book_offer__book', 'book_offer__user')

    context = {
        'popular_offers': popular_offers,
        'new_offers': new_offers,
        'featured_offers': featured_offers,
    }
    return render(request, 'main/index.html', context)


class BookOffersListView(ListView):
    """
    Представление для отображения списка объявлений.
    
    Атрибуты:
        model: Модель BookOffer
        template_name: Шаблон для отображения
        context_object_name: Имя переменной контекста
        paginate_by: Количество объявлений на странице
        
    Методы:
        get_queryset: Возвращает отфильтрованный queryset объявлений
        get_context_data: Добавляет дополнительные данные в контекст
    """
    model = BookOffer
    template_name = 'main/book_offers.html'
    context_object_name = 'offers'
    paginate_by = 12

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset объявлений.
        
        Фильтрует по:
        - Поисковому запросу (если есть)
        - Категории (если выбрана)
        - Статусу публикации
        
        Returns:
            QuerySet: Отфильтрованный список объявлений
        """
        queryset = BookOffer.objects.filter(is_published=True).select_related('book', 'user')
        search_query = self.request.GET.get('search', '')
        category = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(
                Q(book__title__icontains=search_query) |
                Q(book__author__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category:
            queryset = queryset.filter(book__category__name=category)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        
        Добавляет:
        - Поисковый запрос
        - Выбранную категорию
        
        Returns:
            dict: Расширенный контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class BookOfferDetailView(DetailView):
    """
    Представление для отображения детальной информации об объявлении.
    
    Атрибуты:
        model: Модель BookOffer
        template_name: Шаблон для отображения
        context_object_name: Имя переменной контекста
        
    Методы:
        get_context_data: Добавляет дополнительные данные в контекст
    """
    model = BookOffer
    template_name = 'main/book_offer_detail.html'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        
        Добавляет:
        - Фотографии объявления
        - Отзывы об объявлении
        
        Returns:
            dict: Расширенный контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['reviews'] = self.object.reviews.all().select_related('user')
        return context


class BookOfferCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового объявления.
    
    Атрибуты:
        model: Модель BookOffer
        form_class: Форма для создания объявления
        template_name: Шаблон для отображения
        success_url: URL для перенаправления после успешного создания
        
    Методы:
        get_context_data: Добавляет дополнительные данные в контекст
        form_valid: Обрабатывает успешную отправку формы
    """
    model = BookOffer
    form_class = BookOfferForm
    template_name = 'main/book_offer_form.html'
    success_url = reverse_lazy('main:book_offers')

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        
        Добавляет:
        - Набор форм для загрузки фотографий
        
        Returns:
            dict: Расширенный контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = PhotoFormSet()
        return context

    def form_valid(self, form):
        """
        Обрабатывает успешную отправку формы.
        
        Сохраняет:
        - Основную информацию об объявлении
        - Загруженные фотографии
        
        Args:
            form: Валидная форма
            
        Returns:
            HttpResponse: Перенаправление на страницу успеха
        """
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BookOfferUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования объявления.
    
    Атрибуты:
        model: Модель BookOffer
        form_class: Форма для редактирования объявления
        template_name: Шаблон для отображения
        
    Методы:
        get_queryset: Возвращает queryset объявлений текущего пользователя
        get_context_data: Добавляет дополнительные данные в контекст
        form_valid: Обрабатывает успешную отправку формы
    """
    model = BookOffer
    form_class = BookOfferForm
    template_name = 'main/book_offer_form.html'

    def get_queryset(self):
        """
        Возвращает queryset объявлений текущего пользователя.
        
        Returns:
            QuerySet: Объявления текущего пользователя
        """
        return BookOffer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        
        Добавляет:
        - Набор форм для редактирования фотографий
        
        Returns:
            dict: Расширенный контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Обрабатывает успешную отправку формы.
        
        Сохраняет:
        - Обновленную информацию об объявлении
        - Измененные фотографии
        
        Args:
            form: Валидная форма
            
        Returns:
            HttpResponse: Перенаправление на страницу успеха
        """
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BookOfferDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления объявления.
    
    Атрибуты:
        model: Модель BookOffer
        template_name: Шаблон для отображения
        success_url: URL для перенаправления после успешного удаления
        
    Методы:
        get_queryset: Возвращает queryset объявлений текущего пользователя
    """
    model = BookOffer
    template_name = 'main/book_offer_confirm_delete.html'
    success_url = reverse_lazy('main:book_offers')

    def get_queryset(self):
        """
        Возвращает queryset объявлений текущего пользователя.
        
        Returns:
            QuerySet: Объявления текущего пользователя
        """
        return BookOffer.objects.filter(user=self.request.user)
