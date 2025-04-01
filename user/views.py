from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, CreateView

from main.models import BookOffer
from user.forms import LoginUserForm, RegistrationForm
from user.models import Favorite


# Create your views here.
@login_required
@require_http_methods(['POST'])
def toggle_favorite(request):
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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('main:index'))
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('main:index')


def logout_views(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main:index'))
