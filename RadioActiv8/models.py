from django.contrib.gis.db import models
# FIXME: Is this CASCADE line required, given we're referring to 'models.CASCADE' below?
from django.db.models.deletion import CASCADE
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.utils import timezone
import random

# FIXME: This default should be configurable
DEFAULT_POINT = Point(144.63760, -36.49197)


class Base(models.Model):
    name = models.CharField(max_length=128)
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)
    min_patrols = models.IntegerField(blank=True)
    max_patrols = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    def get_intelligence(self, patrol=None):
        """
        Return intelligence available for this base.

        If passed a Patrol, exclude any intelligence that patrol has already
        answered.
        """
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
        if patrol:
            intelligence = Intelligence.objects.filter(
                ~Q(id__in=[
                   i.intelligence.id for i in patrol.patrolanswer_set.all()]),
                base=self)
        else:
            intelligence = Intelligence.objects.filter(base=self)

        return random.choice(list(intelligence))


class Patrol(models.Model):
    name = models.CharField(max_length=128)
    base = models.ForeignKey(
        Base, null=True, blank=True, on_delete=models.PROTECT)
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)

    def __str__(self):
        return self.name

    def check_in(self, base):
        if self.base is not None:
            print(f"Already checked in to {self.base}")
            return False

        self.base = base
        Event(base=self.base, patrol=self).save()
        return True

    def check_out(self, intelligence):
        if self.base is None:
            print("Not checked in")
            return False

        Event(base=self.base, patrol=self, check_out=True).save()
        PatrolAnswer(patrol=self, intelligence=intelligence).save()
        self.base = None
        return True

    def last_seen(self):
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
        return f'{base} {self.question}'


class PatrolAnswer(models.Model):
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    intelligence = models.ForeignKey(Intelligence, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.patrol} answered {self.intelligence.base} base: {self.intelligence.question}'


class Queue(models.Model):
    sequence = models.IntegerField(unique=True)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return str(f'{self.sequence}: {self.patrol} -> {self.base}')


class Event(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    check_out = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        status = 'at' if not self.check_out else 'leaving'
        return f'{self.timestamp}: {self.patrol} {status} {self.base}'
