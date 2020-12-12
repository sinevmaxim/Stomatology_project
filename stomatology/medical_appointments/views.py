from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    StomatologyAppointmentForm,
    StomatologyAppointmentFormDoctor,
)
from django.views.generic import CreateView, ListView, View
from .models import Appointment, WorkingSchedule
from users.models import Doctor
from .decorators import doctor_only


class CreateAppointment(LoginRequiredMixin, CreateView):
    form_class = StomatologyAppointmentForm
    template_name = "medical_appointments/appointment.html"
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
    template_name = "medical_appointments/doctor_appointments.html"

    def get_queryset(self):
        return Appointment.objects.filter(
            doctor_id=Doctor.objects.filter(user_id=self.request.user.id)[0],
            is_closed=False,
        )


@doctor_only
def doctor_update_appointment(request, appointment_id):
    appointment_item = get_object_or_404(Appointment, id=appointment_id)
    if (
        appointment_item.doctor_id
        != Doctor.objects.filter(user_id=request.user.id).first().id
    ):
        messages.warning(request, "Вы не являетесь ведущим врачом для этой формы")
        return redirect("doctor_appointments")

    if appointment_item.is_closed == True:
        messages.warning(
            request,
            "Данная форма уже закрыта и вы не имеете права получить к ней доступ",
        )
        return redirect("doctor_appointments")

    if request.method == "POST":
        form = StomatologyAppointmentFormDoctor(request.POST, instance=appointment_item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Вы завершили прием!")

            return redirect("doctor_appointments")

    form = StomatologyAppointmentFormDoctor(instance=appointment_item)
    context = {"form": form}
    return render(
        request, "medical_appointments/doctor_update_appointment.html", context
    )


class AjaxHandlerView(View):
    def get(self, request):
        doctor_id = request.GET.get("doctor_id")
        dates = WorkingSchedule.objects.filter(
            doctor=doctor_id, is_available=True
        ).all()
        return render(
            request,
            "medical_appointments/dates_dropdown_list_options.html",
            {"dates": dates},
        )
