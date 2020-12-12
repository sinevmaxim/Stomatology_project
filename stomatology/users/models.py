from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    compulsory_health_insurance_policy_number = models.CharField(
        max_length=16,
    )
    phone_number = models.CharField(
        max_length=17,
    )
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"

