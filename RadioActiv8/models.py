from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from django.contrib.gis.geos import Point
from django.db.models import Q
import random

# FIXME: This default should be configurable
DEFAULT_POINT = Point(144.63760, -36.49197)

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

    def get_intelligence(self, patrol=None):
        """
        Return intelligence available for this base.

        If passed a Patrol, exclude any intelligence that patrol has already
        answered.
        """
        # FIXME Update this to work with new model and pull data from Events
        pass
        if patrol:
            return Intelligence.objects.filter(
                ~Q(id__in=[
                   i.intelligence.id for i in patrol.patrolanswer_set.all()]),
                base=self)
        else:
            return Intelligence.objects.filter(base=self)

    def get_random_intelligence(self, patrol=None):
        """
        Return random intelligence for this base.

        If passed a Patrol, exclude any intelligence that patrol has already
        answered.
        """
        # FIXME Update this to work with new model and pull data from Events
        pass
        if patrol:
            intelligence = Intelligence.objects.filter(
                ~Q(id__in=[
                   i.intelligence.id for i in patrol.patrolanswer_set.all()]),
                base=self)
        else:
            intelligence = Intelligence.objects.filter(base=self)

        return random.choice(list(intelligence))

    def get_patrols(self):
        """
        Return a list of patrols currently at this base
        """
        # FIXME Update this to work with new model and pull data from Events
        pass
        return Patrol.objects.filter(base=self)

    def get_patrols_count(self):
        """
        Return an integer representing the number of patrols currently at this base
        """
        # FIXME Update this to work with new model and pull data from Events
        pass
        return self.get_patrols().count()

    def is_full(self):
        """
        Return True if this base is at or over its patrol capacity
        """
        # FIXME Update this to work with new model and pull data from Events
        pass
        if self.max_patrols != 0:
            return self.get_patrols_count() >= self.max_patrols
        else:
            return False


class Patrol(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def check_in(self, base):
        # FIXME Update this to work with new model and pull data from Events
        pass
        if self.base is not None:
            print(f"Already checked in to {self.base}")
            return False

        self.base = base
        Event(base=self.base, patrol=self).save()
        self.save()
        return True

    def log_intelligence(self, base, intelligence):
        # FIXME Update this to work with new model and pull data from Events
        pass

    def log_event(self, base, comment):
        # FIXME Update this to work with new model and pull data from Events
        pass
        Event(base=base, patrol=self, comment=comment)

    def check_out(self):
        # FIXME Update this to work with new model and pull data from Events
        pass
        #Should we assign next base here?
        if self.base is None:
            print("Not checked in")
            return False

        Event(base=self.base, patrol=self, check_out=True).save()
        #PatrolAnswer(patrol=self, intelligence=intelligence).save()
        self.base = None
        self.save()
        return True

    def last_seen(self):
        # FIXME Update this to work with new model and pull data from Events
        pass
        return str(
            Event.objects.filter(
                patrol=self).order_by('-timestamp').first())


class Intelligence(models.Model):
    base = models.ForeignKey(
        Base, blank=True, null=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)

    def __str__(self):
        base = f'{self.base} base:' if self.base else '(no base)'
        return f'{base} {self.question} - {self.answer}'


class Queue(models.Model):
    sequence = models.IntegerField(unique=True)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return str(f'{self.sequence}: {self.patrol} -> {self.base}')


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

    def clean(self):

        # Check Intelligence is valid for this Base
        # FIXME: Should we be explicitly using 'id' below? It didn't work without it
        if self.intelligence_request.base.id != self.location.id:
            raise ValidationError('Can only use Intelligence for current Location')

        # Check that Intelligence hasn't already been allocated to this Patrol
        # FIXME: Deduplicate this code from views.valid_intelligence_options
        patrol_answers = [e.intelligence_request for e in
                      Event.objects.filter(patrol=self.patrol,
                      intelligence_answered_correctly=True).order_by('timestamp')]
        if self.intelligence_request in patrol_answers:
            raise ValidationError("Can only use Intelligence that Patrol hasn't already answered")

    def __str__(self):
        comment = ''
        next_location = ''

        if self.comment:
            comment = ': ' + self.comment
        if self.destination:
            next_location = ', heading to ' + str(self.destination)

        return f'{self.timestamp}: {self.patrol} at {str(self.location)}{next_location}{comment}'


# Game component patrol check-in/out.
