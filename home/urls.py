from django.urls import path

from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
