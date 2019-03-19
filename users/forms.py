from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BeeUser


class BeeUserCreationForm(UserCreationForm):
    """
    Custom form for user creation
    """

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)

    class Meta(UserCreationForm):
        model = BeeUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class BeeUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = BeeUser
        fields = ("username", "email")
