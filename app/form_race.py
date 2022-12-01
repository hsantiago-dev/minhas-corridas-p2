from django.forms import ModelForm
from django import forms
from app.models import Race


class FormRace(ModelForm):

    class Meta:
        model = Race
        fields = [
            'name'
            , 'creator_user'
            , 'registration_deadline'
            , 'start_date'
            , 'distance'
            , 'start_hour'
            , 'registration_value'
            , 'registration_link'
            , 'city'
        ]
        widgets = {
            'registration_deadline': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_hour': forms.TimeInput(attrs={'type': 'time'}),
        }
