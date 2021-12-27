from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from django.contrib.gis.geos import Point
from django.db.models import Q
import random
from django.utils import timezone
from datetime import timedelta

# FIXME: This default should be configurable
DEFAULT_POINT = Point(144.63760, -36.49197)

class GPSTracker(models.Model):
    eui = models.CharField(max_length=16)
    name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    home_base = models.ForeignKey('Base', blank=True, null=True, on_delete=models.SET_NULL, related_name='starts_session')
    # FIXME: Specify a list of session *types*
    #type = 

    def __str__(self):
        return self.name

class Location(models.Model):
    session = models.ManyToManyField(Session)
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)

    def __str__(self):
        if hasattr(self, 'radio'):
            return str(self.radio)
        else:
            return str(self.gps_location)


class Radio(Location):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, null=True)
    channel = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Base(Radio):
    min_patrols = models.IntegerField(blank=True, null=True)
    max_patrols = models.IntegerField(blank=True, null=True)
    run_time = models.DurationField(default=timedelta(minutes=5))
    repeatable = models.BooleanField(default=True)
    attendance_points = models.IntegerField(default=100)

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
        intelligence = Intelligence.objects.filter(base=self)
        if patrol:
            return intelligence.filter(
                ~Q(id__in=[e.intelligence_request.id for e in
                           Event.objects.filter(patrol=patrol,
                                                intelligence_answered_correctly=True).order_by('timestamp')]))
        else:
            return intelligence

    def get_random_intelligence(self, patrol=None):
        """
        Return random intelligence for this base.

        If passed a Patrol, exclude any intelligence that patrol has already
        answered.
        """
        intelligence = self.get_intelligence(patrol)

        return random.choice(intelligence)

    def get_patrols(self):
        """
        Return a list of patrols currently at this base
        """
        return Patrol.objects.filter(current_base=self)

    def get_patrols_via_event(self):
        """
        Return a list of patrols currently at this base
        """
        patrols_at_base = []
        for p in Patrol.objects.all():
            e = p.last_seen()
            if e and e.location and e.location.radio and e.location.radio.base == self:
                patrols_at_base.append(p)
        return patrols_at_base

    def get_patrols_count(self):
        """
        Return an integer representing the number of patrols currently at this base
        """
        return len(self.get_patrols())

    def is_full(self):
        """
        Return True if this base is at or over its patrol capacity
        """
        if self.max_patrols:
            return self.get_patrols_count() >= self.max_patrols
        else:
            return False


class Patrol(models.Model):
    session = models.ManyToManyField(Session)
    name = models.CharField(max_length=128)
    current_base = models.ForeignKey(Base, blank=True, null=True, on_delete=models.SET_NULL)
    attendance_points = models.IntegerField(default=0)
    completion_points = models.IntegerField(default=0)
    bonus_points = models.IntegerField(default=0)
    gps_tracker = models.OneToOneField(GPSTracker, blank=True, null=True, on_delete=models.SET_NULL)

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
        return Event.objects.filter(
                patrol=self).order_by('-timestamp').first()

    def visited_bases(self):
        return Base.objects.filter(id__in = [event.location.id for event in
                self.event_set.all()])

    def get_total_points(self):
        """
        Tally and return different types of points for Patrol
        """
        return self.attendance_points + self.completion_points + self.bonus_points

class Participant(models.Model):
    p_id = models.IntegerField(null=True)
    full_name = models.CharField(max_length=128)
    preferred_name = models.CharField(max_length=128)
    patrol = models.ForeignKey(Patrol, null=True, on_delete=models.SET_NULL)

    PARTICIPANT_TYPE_CHOICES = [
        ('J', 'Joey'),
        ('C', 'Cub'),
        ('S', 'Scout'),
        ('V', 'Venturer'),
        ('R', 'Rover'),
        ('L', 'Leader'),
    ]
    type = models.CharField(
        blank=True, max_length=1, choices=PARTICIPANT_TYPE_CHOICES, default='S')

    def __str__(self):
        return f'({self.p_id}) {self.full_name} - {self.patrol}'

class Intelligence(models.Model):
    base = models.ForeignKey(Base, null=True, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    completion_points = models.IntegerField(default=200)

    def __str__(self):
        base = f'{self.base} base:' if self.base else '(no base)'
        return f'{base} {self.question} - {self.answer} ({self.completion_points})'


class Event(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    intelligence_request = models.ForeignKey(
        Intelligence, blank=True, null=True, on_delete=models.SET_NULL)
    intelligence_answered_correctly = models.BooleanField(default=True)
    destination = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="Destination",
        blank=True, null=True)
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        ordering = ['timestamp']
        constraints = [
            # models.CheckConstraint(check=models.Q(location=intelligence_request.base), name='valid_intelligence_for_base'),
        ]

    def clean(self):

        # Check Intelligence is valid for this Base
        if self.intelligence_request.base != self.location.radio.base:
            raise ValidationError('Can only use Intelligence for current Location')

        # Check that Intelligence hasn't already been allocated to this Patrol
        # FIXME: Deduplicate this code from views.valid_intelligence_options
        patrol_answers = [e.intelligence_request for e in
                      Event.objects.filter(patrol=self.patrol,
                      intelligence_answered_correctly=True).order_by('timestamp')]
        if self.intelligence_request in patrol_answers:
            raise ValidationError("Can only use Intelligence that Patrol hasn't already answered")

        if not self.patrol.session.contains(self.session):
            raise ValidationError(f"Patrol must be part of Event session ({self.session})")

        if not self.location.session.contains(self.session):
            raise ValidationError(f"Location must be part of Event session ({self.session})")

        if not self.destination.session.contains(self.session):
            raise ValidationError(f"Destination must be part of Event session ({self.session})")

    def __str__(self):
        comment = ''
        next_location = ''

        if self.comment:
            comment = ': ' + self.comment
        if self.destination:
            next_location = ', heading to ' + str(self.destination)

        return f'{self.timestamp}: {self.patrol} at {str(self.location)}{next_location}{comment}'