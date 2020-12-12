from django import forms
from django.core.validators import RegexValidator
from .models import Appointment, WorkingSchedule


class StomatologyAppointmentForm(forms.ModelForm):
    queryset = None
    appointment_date = forms.ModelChoiceField(queryset=queryset)

    class Meta:
        model = Appointment
        exclude = ["user", "is_closed", "is_visited", "doctor_comment", "creation_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["appointment_date"].queryset = WorkingSchedule.objects.none()
        if "doctor" in self.data:
            try:
                doctor_id = int(self.data.get("doctor"))
                print(
                    WorkingSchedule.objects.filter(
                        doctor=doctor_id, is_available=True
                    ).order_by("appointment_time")
                )
                self.fields[
                    "appointment_date"
                ].queryset = WorkingSchedule.objects.filter(
                    doctor=doctor_id, is_available=True
                ).order_by(
                    "appointment_time"
                )
            except (ValueError, TypeError):
                pass


class StomatologyAppointmentFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ["doctor", "user", "appointment_date", "comment", "creation_time"]
