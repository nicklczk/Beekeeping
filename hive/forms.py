from django import forms
from .models import Hive


class HiveCreationForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Hive
        fields = ["hive_name"]