from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BeeUser

class BeeUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = BeeUser
        fields = ('username', 'email')

class BeeUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm):
        model = BeeUser
        fields = ('username', 'email')