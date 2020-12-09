from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    StomatologyAppointmentForm,
    StomatologyAppointmentFormDoctor,
)
from django.views.generic import CreateView, ListView
from .models import Appointment, Doctor


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


class ListMyAppointments(LoginRequiredMixin, ListView):
    model = Appointment

    def get_queryset(self):
        return Appointment.objects.filter(user_id=self.request.user.id)


class ListDoctorAppointments(LoginRequiredMixin, ListView):
    model = Appointment

    def get_queryset(self):
        return Appointment.objects.filter(
            doctor_id=Doctor.objects.filter(user_id=self.request.user.id)[0]
        )


# class DoctorUpdateAppointment(LoginRequiredMixin, CreateView):
#     form_class = StomatologyAppointmentFormDoctor
#     template_name = "users/doctor_appointments.html"
#     success_url = reverse_lazy("profile")
#     redirect_field_name = "login"

#     def form_valid(self, form):
#         appointment_form = form.save(commit=False)
#         appointment_form.doctor = self.request.user.doctor

#         appointment_form.save()
#         super().form_valid(form)
#         return HttpResponseRedirect(self.get_success_url())


def doctor_update_appointment(request, appointment_id):
    appointment_item = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        form = StomatologyAppointmentFormDoctor(request.POST, instance=appointment_item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("doctor_appointments")
    form = StomatologyAppointmentFormDoctor(instance=appointment_item)
    context = {"form": form}
    return render(request, "users/doctor_update_appointment.html", context)
