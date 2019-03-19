from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("<username>/", views.profile, name="profile"),
    path("", views.login, name="login"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
