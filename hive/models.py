from django.db import models

from django.db import models
from django.utils import timezone

class Hive(models.Model):
    hive_name = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')
    def __str__(self):
        return self.hive_name 