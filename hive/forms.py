from django import forms
from .models import Hive, HiveTimeline

import datetime


class HiveCreationForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Hive
        fields = ["hive_name"]


def pastDate(date):
    if date > datetime.date.today():
        raise forms.ValidationError("The date cannot be in the future!")
    return date


class EntryCreationForm(forms.ModelForm):

    timeline_date = forms.DateField(label='Timeline Date:', 
                                    widget=forms.SelectDateWidget(years=[x for x in range(datetime.datetime.now().year,1950,-1)]),
                                    validators=[pastDate])

    class Meta(forms.ModelForm):
        model = HiveTimeline
        fields = ["timeline_date", "brood_cells", "honey_racks", "hive_size",
                  "queen_spotted", "pests_disease", "plant_life"]