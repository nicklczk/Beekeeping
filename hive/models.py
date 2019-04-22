from django.db import models

from django.db import models
from django.utils import timezone

# Model that represents a hive
class Hive(models.Model):
    hive_name = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    creation_date = models.DateTimeField("date created")

    def __str__(self):
        return self.hive_name


# Model that represents a timeline event for a hive
class HiveTimeline(models.Model):
    hive_name = models.CharField(max_length=200)
    hive_key = models.IntegerField(default=0)
    user = models.CharField(max_length=200)
    creation_date = models.DateTimeField("date created")
    edited_date = models.DateTimeField("date edited")
    timeline_date = models.DateField("timeline date")
    brood_cells = models.IntegerField(default=0)
    honey_racks = models.IntegerField(default=0)
    hive_size = models.IntegerField(default=0)
    queen_spotted = models.BooleanField()
    pests_disease = models.BooleanField()
    plant_life = models.BooleanField()

    temperature = models.DecimalField(default=0, decimal_places=2, max_digits=4)

    def __str__(self):
        return str(self.timeline_date.strftime("%Y-%m-%d"))
    
# models.py 
class Image(models.Model): 
    timeline_key = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/')     
