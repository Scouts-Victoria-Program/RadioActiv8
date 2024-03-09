from django.forms import ModelForm, Textarea
from django import forms
from .models import Base, Patrol, Event, Session, GPSTracker
import random


class BaseForm(ModelForm):
    class Meta:
        model = Base
        fields = ("name", "min_patrols", "max_patrols", "activity_type", "channel")


# class PatrolForm(ModelForm):
#     class Meta:
#         model = Patrol
#         fields = ("name",)


class EventForm(ModelForm):
    class Media:
        js = ("RadioActiv8/js/event-form.js",)

    class Meta:
        model = Event
        fields = (
            "session",
            "patrol",
            "location",
            "intelligence_request",
            "intelligence_answered_correctly",
            "destination",
            "comment",
        )
        widgets = {
            "session": forms.widgets.Select(attrs={"class": "btn-sm"}),
            "patrol": forms.widgets.Select(attrs={"class": "btn-lg"}),
            "location": forms.widgets.Select(attrs={"class": "btn-sm"}),
            "intelligence_request": forms.widgets.Select(attrs={"class": "btn-sm"}),
            # 'intelligence_answered_correctly': forms.widgets.Select(attrs={'class': 'btn-sm'}),
            "destination": forms.widgets.Select(attrs={"class": "btn-sm"}),
            "comment": Textarea(attrs={"cols": 40, "rows": 3}),
        }


class BonusPointsForm(forms.Form):
    patrol = forms.ModelChoiceField(
        queryset=Patrol.objects.all(), widget=forms.widgets.HiddenInput
    )
    bonus_points = forms.IntegerField(
        label="Bonus Points",
        initial=0,
        widget=forms.widgets.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
    )


class SessionListForm(forms.Form):
    session_list_field = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Session",
    )


class SessionAddPatrolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        session = kwargs.pop("session")
        super(SessionAddPatrolForm, self).__init__(*args, **kwargs)
        bases = Base.objects.all().filter(session=session)
        if session.home_base:
            bases = bases.exclude(id=session.home_base.id)
        random_base = random.choice(bases)
        self.fields["base"] = forms.ModelChoiceField(
            queryset=bases, initial=random_base
        )

    ra8_session = forms.ModelChoiceField(
        queryset=Session.objects.all(), widget=forms.widgets.HiddenInput
    )
    patrol = forms.ModelChoiceField(queryset=Patrol.objects.all())
    gps_tracker = forms.ModelChoiceField(
        queryset=GPSTracker.objects.filter(patrol=None), label="GPS Tracker"
    )


class GPSTrackerPatrolForm(forms.Form):
    gpstracker = forms.ModelChoiceField(
        queryset=GPSTracker.objects.all(),
        label="GPS Tracker",
        widget=forms.widgets.HiddenInput,
    )
    patrol = forms.ModelChoiceField(queryset=Patrol.objects.all(), required=False)


class PatrolForm(forms.Form):
    patrol = forms.ModelChoiceField(queryset=Patrol.objects.all())
