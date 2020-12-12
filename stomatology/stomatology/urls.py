from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.decorators import unauthenticated_user, chip_number_needed
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", user_views.register, name="register"),
    path("", include("home.urls")),
    path(
        "login/",
        unauthenticated_user(
            auth_views.LoginView.as_view(template_name="users/login.html")
        ),
        name="login",
    ),
    path(
        "logout/",
        login_required(
            auth_views.LogoutView.as_view(template_name="users/logout.html")
        ),
        name="logout",
    ),
    path("profile/", user_views.profile, name="profile"),
    path("profile/update", user_views.update_profile, name="update_profile"),
    path("appointments/", include("medical_appointments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
