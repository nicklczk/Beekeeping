from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("<username>/viewhives", views.viewhives, name="viewhives"),
    path("<username>/createhive", views.createhive, name="createhive"),
    path("<username>/<hive_pk>", views.viewhive, name="viewhive"),
    path("<username>/<hive_pk>/delete", views.deletehive, name="deletehive"),
    path("<username>/<hive_pk>/edit", views.edithive, name="edithive"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)