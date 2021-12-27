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
    session_list_field = forms.ModelChoiceField(queryset=Session.objects.all(), widget=forms.Select,  label='Session')

