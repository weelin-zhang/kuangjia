"""web1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic  import RedirectView
from django.conf import settings
from .views import *

#sso_url = 'http://192.168.20.37:8000/accounts/login/'
print(settings.SSO_AUTH_URL)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', RedirectView.as_view(url=settings.SSO_AUTH_URL,permanent=True, query_string=True), name='login'),
    url(r'^logout/(?P<authtoken>.*)/$', logout, name='logout'),
    url(r'^$', IndexView.as_view(), name='index'),
]
