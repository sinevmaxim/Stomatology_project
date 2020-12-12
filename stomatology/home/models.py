from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, max_length=500)
    image = models.ImageField(default="default_news.jpg", upload_to="profile_pics")
    creation_time = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    price = models.PositiveIntegerField()
