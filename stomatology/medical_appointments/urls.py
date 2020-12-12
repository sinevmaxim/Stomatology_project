from django.urls import path, include
from .views import (
    CreateAppointment,
    ListMyAppointments,
    ListDoctorAppointments,
    AjaxHandlerView,
    doctor_update_appointment,
)
from medical_appointments.decorators import doctor_only
from users.decorators import chip_number_needed


urlpatterns = [
    path(
        "create",
        chip_number_needed(CreateAppointment.as_view()),
        name="appointment",
    ),
    path(
        "my_appointments",
        ListMyAppointments.as_view(),
        name="my_appointments",
    ),
    path(
        "doctor_appointments",
        doctor_only(ListDoctorAppointments.as_view()),
        name="doctor_appointments",
    ),
    path(
        "doctor_appointments/<int:appointment_id>/",
        doctor_update_appointment,
        name="doctor_appointment_update",
    ),
    path("doctor_form_change_ajax", AjaxHandlerView.as_view(), name="ajax_appointment"),
]
