from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from datetime import date
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse


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


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey("Doctor", on_delete=models.PROTECT)
    comment = models.TextField(blank=True, max_length=500)
    is_closed = models.BooleanField(default=False)
    is_visited = models.BooleanField(default=False)
    doctor_comment = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f"Запись {self.user.last_name} {self.user.first_name} к {self.doctor} на {self.appointment_date}"

    def get_absolute_url(self):
        return reverse("appointment", kwargs={"pk": self.pk})


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class WorkingSchedule(models.Model):
    time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE)
