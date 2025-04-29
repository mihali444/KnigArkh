"""
URL configuration for KnigArch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from login.views import UserLoginView, logout_views
from registration.views import UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('announcement/', include('book.urls')),
    path('profile/', include('user.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_views, name='logout'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('reset-password/', include('rest_password.urls')),
    path('', include('main.urls')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


