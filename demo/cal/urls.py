from django.conf.urls import url, include
from django.views.generic import TemplateView

from cal import views

urlpatterns = [
    url(r'^', include('swingtime.urls')),
    url(r'^events/type/([^/]+)/$', views.event_type, name='karate-event'),
]
