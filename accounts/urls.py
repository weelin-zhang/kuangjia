from django.conf.urls import url
from django.contrib.auth.views import login, logout # 方法被废弃
from django.contrib.auth.views import LoginView, LogoutView
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm

urlpatterns = [
    # 被废弃
    # url(r'^login/$', login, {'authentication_form': LoginForm, 'template_name': 'accounts/login.html'}, name='login'),
    # url(r'^logout/$', logout, {'next_page': reverse_lazy('accounts:login')}, name='logout'),


    url(r'^login/$', LoginView.as_view(**{"authentication_form": LoginForm, 'template_name': 'accounts/login.html'}), name='login'),
    url(r'^logout/$', LogoutView.as_view(**{'next_page': reverse_lazy('accounts:login')}), name='logout'),
]
