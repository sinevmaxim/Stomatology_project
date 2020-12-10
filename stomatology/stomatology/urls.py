from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import (
    CreateAppointment,
    ListMyAppointments,
    ListDoctorAppointments,
    AjaxHandlerView,
)
from users.decorators import doctor_only

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", user_views.register, name="register"),
    path("", include("home.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("profile/", user_views.profile, name="profile"),
    path("appointment/", CreateAppointment.as_view(), name="appointment"),
    path("my_appointments/", ListMyAppointments.as_view(), name="my_appointments"),
    path(
        "doctor_appointments/",
        doctor_only(ListDoctorAppointments.as_view()),
        name="doctor_appointments",
    ),
    path(
        "doctor_appointments/<int:appointment_id>/",
        user_views.doctor_update_appointment,
        name="doctor_appointment_update",
    ),
    path("ajax/appointment", AjaxHandlerView.as_view(), name="ajax_appointment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
