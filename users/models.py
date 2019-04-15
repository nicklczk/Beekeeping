from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class BeeUser(AbstractUser):
    """
    BeeUser

    Extends Django AbstractUser which provides access to common
    default values, such as username, email, etc
    """

    zipcode = models.SmallIntegerField(default="00000")

    def __str__(self):
        return self.email
