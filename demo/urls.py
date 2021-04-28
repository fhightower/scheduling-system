from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/cal/')),
    url(r'^cal/', include('cal.urls')),
]
