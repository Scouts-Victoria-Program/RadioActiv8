from django.forms import ModelForm
from django import forms
from .models import *


class BaseForm(ModelForm):
    class Meta:
        model = Base
        fields = ('name', 'min_patrols', 'max_patrols', 'activity_type', 'channel')

class PatrolForm(ModelForm):
    class Meta:
        model = Patrol
        fields = ('name',)

class EventForm(ModelForm):
    class Media:
        js = ('RadioActiv8/js/event-form.js',)
    class Meta:
        model = Event
        fields = ('session', 'patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')

class SessionListForm(forms.Form):

    CHOICES = [ (s.id, s.name) for s in Session.objects.all() ]
    session_list_field = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label='Session', initial='')