from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import BeeUserCreationForm, BeeUserChangeForm
from .models import BeeUser

# Register your models here.


class BeeUserAdmin(UserAdmin):
    add_form = BeeUserCreationForm
    form = BeeUserChangeForm
    model = BeeUser
    list_display = ["email", "username"]


admin.site.register(BeeUser, BeeUserAdmin)
