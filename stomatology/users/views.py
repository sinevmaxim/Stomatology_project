from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    StomatologyAppointmentForm,
)
from django.views.generic import CreateView


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
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
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)


class CreateAppointment(LoginRequiredMixin, CreateView):
    form_class = StomatologyAppointmentForm
    template_name = "users/appointment.html"
    success_url = reverse_lazy("profile")
    redirect_field_name = "login"

    def form_valid(self, form):
        appointment_form = form.save(commit=False)
        appointment_form.user = self.request.user
        appointment_form.save()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())
