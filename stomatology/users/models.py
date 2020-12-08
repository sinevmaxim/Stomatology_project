from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    compulsory_health_insurance_policy_regex = RegexValidator(
        regex=r"\d{16}",
        message="CHI Policy number should contain 16 digits and entered in the following format: '1111111111111111'.",
    )
    compulsory_health_insurance_policy_number = models.CharField(
        validators=[compulsory_health_insurance_policy_regex],
        max_length=16,
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
    )
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"Профиль {self.user}"
