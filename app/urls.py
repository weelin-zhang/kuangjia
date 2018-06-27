from django.conf.urls import url
# from django.core.urlresolvers import reverse_lazy
from .views import *
urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name="app_index"),
]
