from django.contrib.gis.db import models
from django.db.models.deletion import CASCADE
from django.contrib.gis.geos import Point

# FIXME: This default should be configurable
DEFAULT_POINT = Point(144.63760,-36.49197)

class Patrol(models.Model):
    name = models.CharField(max_length=128)
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)

    def __str__(self):
        return self.name

class Base(models.Model):
    name = models.CharField(max_length=128)
    gps_location = models.PointField(blank=True, default=DEFAULT_POINT)
    min_patrols = models.IntegerField(blank=True)
    max_patrols = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

class Intelligence(models.Model):
    base = models.ForeignKey(Base, blank=True, null=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)

    def __str__(self):
        base = f'{self.base} base:' if self.base else '(no base)' 
        return f'{base} {self.question}'

class Queue(models.Model):
    sequence = models.IntegerField(unique=True)
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.sequence}: {self.patrol} -> {self.base}')

class Event(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    check_out = models.BooleanField()
    intelligence = models.ForeignKey(Intelligence, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.timestamp}: {self.patrol} at {self.base}, answering {self.intelligence}'