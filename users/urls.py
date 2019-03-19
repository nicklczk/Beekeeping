from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("", views.login, name="login"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
