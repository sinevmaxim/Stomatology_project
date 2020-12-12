from django.shortcuts import render
from django.views.generic import ListView
from .models import News


class NewsList(ListView):
    model = News
    template_name = "home/index.html"
    paginate_by = 10

    def get_queryset(self):
        return News.objects.all()


def about(request):
    return render(request, "home/about.html")
