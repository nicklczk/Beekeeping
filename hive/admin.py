from django.contrib import admin
from .models import Hive, HiveTimeline, Image

# Register your models here.

admin.site.register(Hive)
admin.site.register(HiveTimeline)
admin.site.register(Image)
