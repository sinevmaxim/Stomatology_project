from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Appointment
from users.models import Doctor
from django.contrib import messages


def doctor_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if Doctor.objects.filter(user_id=request.user.id).first() is None:
            return redirect("my_appointments")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func