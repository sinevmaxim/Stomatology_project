from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


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
    return render(request, "users/profile.html")