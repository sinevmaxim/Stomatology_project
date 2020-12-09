from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Profile, Doctor, Appointment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"placeholder": ("Юзернейм")})
        self.fields["first_name"].widget.attrs.update({"placeholder": ("Имя")})
        self.fields["last_name"].widget.attrs.update({"placeholder": ("Фамилия")})
        self.fields["email"].widget.attrs.update({"placeholder": ("Email")})
        self.fields["password1"].widget.attrs.update({"placeholder": ("Пароль")})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": ("Повторите пароль")}
        )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class ProfileUpdateForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    compulsory_health_insurance_policy_regex = RegexValidator(
        regex=r"\d{16}",
        message="CHI Policy number should contain 16 digits and entered in the following format: '1111111111111111'.",
    )
    compulsory_health_insurance_policy_number = forms.CharField(
        validators=[compulsory_health_insurance_policy_regex],
        max_length=17,
        label=("Compulsory Health Insurance policy number"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "required": "true",
            }
        ),
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        label=("Phone number"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "required": "true",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = [
            "image",
            "compulsory_health_insurance_policy_number",
            "phone_number",
        ]


class StomatologyAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ["user", "is_closed", "is_visited", "doctor_comment"]


class StomatologyAppointmentFormDoctor(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ["doctor","user", "appointment_date", "comment"]