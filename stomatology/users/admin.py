from django.contrib import admin
from .models import Appointment, Doctor, Profile

admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Appointment)