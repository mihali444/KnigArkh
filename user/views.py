from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, FormView

from main.models import BookOffer
from user.forms import ProfileEditForm
from user.models import Reviews, Favorite, Subscriber


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
