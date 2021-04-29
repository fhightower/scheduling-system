from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', include('swingtime.urls'))
]
