from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView

from profile.forms import LoginUserForm, RegistrationForm


# Create your views here.
class UserRegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'profile/registration.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = 'profile/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('main:index')


def logout_views(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main:index'))
