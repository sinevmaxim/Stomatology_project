from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import Profile
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            last_name = form.cleaned_data.get("last_name")
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request,
                f"Зарегестрирован пользователь с именем {last_name} {first_name}. Войдите, чтобы начать работу",
            )

            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    context = {
        "user": request.user,
    }
    return render(request, "users/profile.html", context)


@login_required
def update_profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Ваш аккаунт усмешно изменен")

            return redirect("profile")

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/update_profile.html", context)