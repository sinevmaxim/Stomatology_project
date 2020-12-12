from django import forms
from django.core.validators import RegexValidator
from .models import Appointment, WorkingSchedule


class StomatologyAppointmentForm(forms.ModelForm):
    queryset = None
    appointment_date = forms.ModelChoiceField(queryset=queryset)

    class Meta:
        model = Appointment
        exclude = ["user", "is_closed", "is_visited", "doctor_comment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        items = WorkingSchedule.objects.none()

        self.fields["appointment_date"].queryset = items
        if "doctor" in self.data:
            try:
                doctor_id = int(self.data.get("doctor"))
                self.fields[
                    "appointment_date"
                ].queryset = WorkingSchedule.objects.filter(
                    doctor=doctor_id, is_available=True
                ).order_by(
                    "time"
                )
            except (ValueError, TypeError):
                pass


class StomatologyAppointmentFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ["doctor", "user", "appointment_date", "comment"]
