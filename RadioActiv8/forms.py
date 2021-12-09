from django.forms import ModelForm
from django import forms
from .models import *


class BaseForm(ModelForm):
    class Meta:
        model = Base
        fields = ('location_name', 'min_patrols', 'max_patrols', 'activity_type', 'channel')

class PatrolForm(ModelForm):
    class Meta:
        model = Patrol
        fields = ('name',)

class EventForm(ModelForm):
    comment = forms.CharField( widget=forms.Textarea )
    class Media:
        js = ('assets/js/event-form.js',)
    class Meta:
        model = Event
        fields = ('patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')