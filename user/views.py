from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, FormView, ListView, DetailView, UpdateView, CreateView

from main.models import BookOffer
from user.forms import ProfileEditForm
from user.models import Reviews, Favorite, Subscriber


@login_required
@require_http_methods(['POST'])
def upload_photo(request):
    if 'photo' not in request.FILES:
        return JsonResponse({
            'status': 'error',
            'message': 'No photo file provided'
        }, status=400)

    try:
        user = request.user
        photo = request.FILES['photo']

        # Save the new photo to the user's profile
        user.photo = photo
        user.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Photo uploaded successfully',
            'photo_url': user.photo.url
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@require_http_methods(['POST'])
def subscribe(request, ):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется вход в систему'},
            status=403
        )

    subscriber_id = request.POST.get('subscriber_id')
    subscriber_to_id = request.POST.get('subscriber_to_id')

    try:
        subscriber = get_user_model().objects.get(id=subscriber_id)
        subscriber_to = get_user_model().objects.get(id=subscriber_to_id)

        subscribe, created = Subscriber.objects.get_or_create(subscriber=subscriber, subscribed_to=subscriber_to)

        if not created:
            subscribe.delete()
            is_subscribed = False
        else:
            is_subscribed = True

        return JsonResponse({'status': 'success', 'is_subscribed': is_subscribed})
    except get_user_model().DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=404)


class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'profile/change-password.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse('profile:profile', kwargs={'username': self.request.user.username})


# Create your views here.
class ProfileEditView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'profile/profile-edit.html'
    form_class = ProfileEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        changed_data = form.changed_data  # Список полей, которые были изменены

        if 'first_name' in changed_data:
            user.first_name = form.cleaned_data['first_name']
        if 'last_name' in changed_data:
            user.last_name = form.cleaned_data['last_name']
        if 'date_of_birth' in changed_data:
            user.date_of_birth = form.cleaned_data['date_of_birth']
        if 'username' in changed_data:
            user.username = form.cleaned_data['username']

        if changed_data:
            user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile:profile', kwargs={'username': self.request.user.username})


class ProfileView(TemplateView):
    template_name = 'profile/my_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(get_user_model(), username=kwargs['username'])
        if user:
            context['user'] = user

            reviews = Reviews.objects.filter(
                offer__user=user
            ).select_related('offer', 'user')

            grade_counts = {}
            for review in reviews:
                grade_counts[review.grade] = grade_counts.get(review.grade, 0) + 1

            context['reviews'] = [{'grade': grade, 'grade__count': count}
                                 for grade, count in grade_counts.items()]

            context['total_review'] = len(reviews)
            context['total_comments'] = sum(1 for review in reviews if review.description and review.description.strip())

            context['rating_data'] = {
                'reviews': [
                    {'rating': review.grade} for review in reviews
                ],
                'comments': [
                    {'text': review.description} for review in reviews
                    if review.description and review.description.strip()
                ]
            }

            request_user = self.request.user
            user_favorites = set()
            if request_user.is_authenticated:
                user_favorites = set(
                    Favorite.objects.filter(user=request_user).values_list('offer_id', flat=True)
                )
            context['user_favorites'] = user_favorites

            book_offers_query = BookOffer.objects.filter(
                user=user
            ).select_related(
                'book',
                'book__author',
            ).prefetch_related(
                'book__photos',
                'photos'
            ).order_by(
                '-date_created'
            )

            active_offers = book_offers_query.filter(
                is_active='Active',
                is_published=True,
            )

            complete_offers = book_offers_query.filter(
                is_active='Completed',
            )

            for offer in active_offers:
                offer.first_photo = offer.photos.first()

            for offer in complete_offers:
                offer.first_photo = offer.photos.first()

            context['active'] = active_offers
            context['complete'] = complete_offers

            # Check if the current user is subscribed to the profile user
            is_subscribed = False
            if request_user.is_authenticated and request_user != user:
                is_subscribed = Subscriber.objects.filter(
                    subscriber=request_user,
                    subscribed_to=user
                ).exists()
            context['is_subscribed'] = is_subscribed

            return context
        return Http404()


class UserLoginView(LoginView):
    """
    Представление для входа пользователя в систему.
    
    Атрибуты:
        template_name: Шаблон страницы входа
        redirect_authenticated_user: Перенаправление авторизованных пользователей
    """
    template_name = 'user/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.
    
    Атрибуты:
        next_page: URL для перенаправления после выхода
    """
    next_page = reverse_lazy('main:index')


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Представление профиля пользователя.
    
    Атрибуты:
        model: Модель User
        template_name: Шаблон профиля
        context_object_name: Имя переменной контекста
        
    Методы:
        get_context_data: Добавляет дополнительные данные в контекст
    """
    model = get_user_model()
    template_name = 'user/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст.
        
        Добавляет:
        - Объявления пользователя
        - Отзывы пользователя
        - Количество подписчиков
        - Количество подписок
        
        Returns:
            dict: Расширенный контекст шаблона
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['offers'] = user.bookoffer_set.all()
        context['reviews'] = user.reviews.all()
        context['subscribers_count'] = user.subscribers.count()
        context['subscriptions_count'] = user.subscriptions.count()
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя.
    
    Атрибуты:
        model: Модель User
        template_name: Шаблон формы редактирования
        fields: Поля для редактирования
        success_url: URL для перенаправления после успешного обновления
        
    Методы:
        get_object: Возвращает объект для редактирования
    """
    model = get_user_model()
    template_name = 'user/profile_update.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_of_birth']
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        """
        Возвращает объект для редактирования.
        
        Returns:
            User: Текущий пользователь
        """
        return self.request.user


class FavoriteListView(LoginRequiredMixin, ListView):
    """
    Представление списка избранных объявлений.
    
    Атрибуты:
        model: Модель Favorite
        template_name: Шаблон списка избранного
        context_object_name: Имя переменной контекста
        
    Методы:
        get_queryset: Возвращает queryset избранных объявлений
    """
    model = Favorite
    template_name = 'user/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        """
        Возвращает queryset избранных объявлений.
        
        Returns:
            QuerySet: Избранные объявления текущего пользователя
        """
        return Favorite.objects.filter(user=self.request.user).select_related('offer', 'offer__book')


def toggle_favorite(request, offer_id):
    """
    Функция для добавления/удаления объявления из избранного.
    
    Args:
        request: HTTP запрос
        offer_id: ID объявления
        
    Returns:
        HttpResponse: Перенаправление на страницу объявления
    """
    offer = get_object_or_404(BookOffer, id=offer_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, offer=offer)
    
    if not created:
        favorite.delete()
        
    return redirect('main:book_offer_detail', pk=offer_id)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания отзыва.
    
    Атрибуты:
        model: Модель Reviews
        template_name: Шаблон формы отзыва
        fields: Поля для заполнения
        success_url: URL для перенаправления после успешного создания
        
    Методы:
        form_valid: Обрабатывает успешную отправку формы
    """
    model = Reviews
    template_name = 'user/review_form.html'
    fields = ['grade', 'description']
    success_url = reverse_lazy('main:book_offers')

    def form_valid(self, form):
        """
        Обрабатывает успешную отправку формы.
        
        Сохраняет:
        - Отзыв с привязкой к пользователю и объявлению
        
        Args:
            form: Валидная форма
            
        Returns:
            HttpResponse: Перенаправление на страницу успеха
        """
        form.instance.user = self.request.user
        form.instance.offer_id = self.kwargs['offer_id']
        return super().form_valid(form)


class SubscriberListView(LoginRequiredMixin, ListView):
    """
    Представление списка подписчиков пользователя.
    
    Атрибуты:
        model: Модель Subscriber
        template_name: Шаблон списка подписчиков
        context_object_name: Имя переменной контекста
        
    Методы:
        get_queryset: Возвращает queryset подписчиков
    """
    model = Subscriber
    template_name = 'user/subscribers.html'
    context_object_name = 'subscribers'

    def get_queryset(self):
        """
        Возвращает queryset подписчиков.
        
        Returns:
            QuerySet: Подписчики текущего пользователя
        """
        return Subscriber.objects.filter(subscribed_to=self.request.user).select_related('subscriber')


def toggle_subscription(request, user_id):
    """
    Функция для подписки/отписки от пользователя.
    
    Args:
        request: HTTP запрос
        user_id: ID пользователя
        
    Returns:
        HttpResponse: Перенаправление на профиль пользователя
    """
    user_to_subscribe = get_object_or_404(get_user_model(), id=user_id)
    
    if request.user != user_to_subscribe:
        subscription, created = Subscriber.objects.get_or_create(
            subscriber=request.user,
            subscribed_to=user_to_subscribe
        )
        
        if not created:
            subscription.delete()
            
    return redirect('user:profile', pk=user_id)
