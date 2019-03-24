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
    path("<username>/<hive_pk>/addentry", views.addtimelineentry, name="addtimelineentry"),
    path("<username>/<hive_pk>/<timeline_pk>", views.viewtimelineentry, name="viewtimelineentry"),
    path("<username>/<hive_pk>/<timeline_pk>/delete", views.deleteevent, name="deleteevent"),
    path("<username>/<hive_pk>/<timeline_pk>/edit", views.editevent, name="editevent"),
    path("<username>/<hive_pk>/<data_type>/graphdata", views.graphdata, name="graphdata"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)