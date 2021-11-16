from django.forms import ModelForm
from .models import *


class BaseForm(ModelForm):
    class Meta:
        model = Base
        fields = ('location_name', 'min_patrols', 'max_patrols', 'activity_type', 'channel')

class PatrolForm(ModelForm):
    class Meta:
        model = Patrol
        fields = ('name',)
