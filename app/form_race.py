from django.forms import ModelForm
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
