from django.urls import path
from . import views
from .views import NewsList


urlpatterns = [
    path("", NewsList.as_view(), name="home"),
    path("about", views.about, name="about"),
]
