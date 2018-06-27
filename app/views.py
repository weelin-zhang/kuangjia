from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
# Create your views here.


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "app/index.html")