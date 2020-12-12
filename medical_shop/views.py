from django.shortcuts import render
from django.views.generic import ListView
from .models import News


class NewsList(ListView):
    model = News

    def get_queryset(self):
        return News.objects.all()
