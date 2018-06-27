from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin

class HomeView(LoginRequiredMixin, CommonMixin, View):
    template_name = 'home.html'
    page_title = '概述'

    def get(self, request):
        return render(request, self.template_name)