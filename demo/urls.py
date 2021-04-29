from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView

from views import login

urlpatterns = [
    url(r'^$', login),
    url(r'^cal/', include('cal.urls')),
]
