from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Doctor, Appointment
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def doctor_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if Doctor.objects.filter(user_id=request.user.id).first() is None:
            return redirect("my_appointments")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def chip_number_needed(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.compulsory_health_insurance_policy_number == "":
            messages.warning(
                request,
                "Для того чтобы записаться на приём необходимо заполнить номер полиса ОМС",
            )
            return redirect("update_profile")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func