from django.forms import ModelForm
from django import forms
from .models import *
import random


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
    session_list_field = forms.ModelChoiceField(queryset=Session.objects.all(), widget=forms.Select, label='Session')

class SessionAddPatrolForm(forms.Form):
    def __init__(self, data, *args, **kwargs):
        super(SessionAddPatrolForm, self).__init__(*args, **kwargs)
        session = data['session']
        bases = Base.objects.all().filter(session=session)
        if session.home_base:
            bases = bases.exclude(id=session.home_base.id)
        random_base = random.choice(bases)
        self.fields['base'] = forms.ModelChoiceField(queryset=bases, initial=random_base)

    session = forms.ModelChoiceField(queryset=Session.objects.all(), widget=forms.widgets.HiddenInput)
    patrol = forms.ModelChoiceField(queryset=Patrol.objects.all())
    gps_tracker = forms.ModelChoiceField(queryset=GPSTracker.objects.filter(patrol=None), label='GPS Tracker')
