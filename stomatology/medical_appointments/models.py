from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Doctor


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    comment = models.TextField(blank=True, max_length=500)
    is_closed = models.BooleanField(default=False)
    is_visited = models.BooleanField(default=False)
    doctor_comment = models.TextField(blank=True, max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запись {self.user.last_name} {self.user.first_name} к {self.doctor} на {self.appointment_date}"

    def get_absolute_url(self):
        return reverse("appointment", kwargs={"pk": self.pk})


class WorkingSchedule(models.Model):
    appointment_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment_time}"
