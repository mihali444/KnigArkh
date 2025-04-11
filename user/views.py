from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, TemplateView

from main.models import BookOffer
from user.forms import LoginUserForm, RegistrationForm
from user.models import Favorite, Reviews


# Create your views here.
@require_http_methods(['POST'])
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется вход в систему'},
            status=403
        )

    offer_id = request.POST.get('offer_id')
    try:
        offer = BookOffer.objects.get(id=offer_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, offer=offer)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
        return JsonResponse({'status': 'success', 'is_favorite': is_favorite})
    except BookOffer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Книга не найдена'}, status=404)


class UserRegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'profile/registration.html'
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main:index'))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = 'profile/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main:index'))
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', self.get_default_redirect_url())


def logout_views(request):
    next_page = request.GET.get('next', request.path)
    logout(request)
    return HttpResponseRedirect(next_page or reverse('main:index'))


class UserResetPasswordView(PasswordResetView):
    template_name = 'profile/password-reset.html'
    form_class = PasswordResetForm
    html_email_template_name = 'profile/password_reset_email.html'
    success_url = reverse_lazy('profile:password-reset-done')


class UseerPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'profile/enter-email.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'profile/new-password.html'
    success_url = reverse_lazy('profile:login')


class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = BookOffer.objects.filter(
            user=self.request.user,
            is_active='Active',
            is_published=True,
        ).select_related(
            'book',
            'book__author',
        ).prefetch_related(
            'book__photos',
            'photos'
        ).order_by(
            '-date_created'
        )

        context['complete'] = BookOffer.objects.filter(
            user=self.request.user,
            is_active='Completed',
            # is_published=False,
        ).select_related(
            'book',
            'book__author',
        ).prefetch_related(
            'book__photos',
            'photos'
        ).order_by(
            '-date_created'
        )

        context['reviews'] = Reviews.objects.filter(
            offer__user=self.request.user
        ).values(
            'grade'
        ).annotate(
            Count('grade')
        )

        context['total_comments'] = Reviews.objects.filter(
            offer__user=self.request.user,
            description__isnull=False
        ).exclude(
            description=''
        ).count()

        context['total_review'] = Reviews.objects.filter(
            offer__user=self.request.user,
        ).count()

        return context

