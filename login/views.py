from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from login.forms import LoginUserForm


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'login/login.html'
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
