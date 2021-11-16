from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from django.contrib.gis.geos import Point
from django.db.models import Q
import random

# FIXME: This default should be configurable
DEFAULT_POINT = Point(144.63760, -36.49197)

'''
# Location, welfare, logistics etc.

# Primarily we have a logging system.
'''


class Location(models.Model):
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)

    def __str__(self):
        if hasattr(self, 'radio'):
            return str(self.radio)
        else:
            return str(self.gps_location)


class Radio(Location):
    location_name = models.CharField(max_length=128)
    channel = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.location_name


class Base(Radio):
    min_patrols = models.IntegerField(blank=True, null=True)
    max_patrols = models.IntegerField(blank=True, null=True)
    ACTIVITY_TYPE_CHOICES = [
        ('R', 'Reading data'),
        ('S', 'Self-directed'),
        ('F', 'Facilitated'),
    ]
    activity_type = models.CharField(
        blank=True, max_length=1, choices=ACTIVITY_TYPE_CHOICES, default='S')


class Patrol(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Intelligence(models.Model):
    base = models.ForeignKey(
        Base, blank=True, null=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)

    def __str__(self):
        base = f'{self.base} base:' if self.base else '(no base)'
        return f'{base} {self.question} - {self.answer}'

'''

Need to filter available intelligence based on
(a) which base this is, and
(b) which intelligence this patrol has not answered

'''

class Event(models.Model):
    # TODO: Allow manually setting and editing of timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    intelligence_request = models.ForeignKey(
        Intelligence, blank=True, null=True, on_delete=models.SET_NULL)
    intelligence_answered_correctly = models.BooleanField(default=False)
    destination = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="Destination",
        blank=True, null=True)
    comment = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        constraints = [
            # models.CheckConstraint(check=models.Q(location=intelligence_request.base), name='valid_intelligence_for_base'),
        ]

    def __str__(self):
        comment = ''
        next_location = ''

        if self.comment:
            comment = ': ' + self.comment
        if self.destination:
            next_location = ', heading to ' + str(self.destination)

        return f'{self.timestamp}: {self.patrol} at {str(self.location)}{next_location}{comment}'


# Game component patrol check-in/out.
