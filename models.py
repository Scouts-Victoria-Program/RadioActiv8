from django.contrib.gis.db import models
from django.db.models.deletion import CASCADE

class Patrol(models.Model):
    name = models.CharField(max_length=32)
    gps_location = models.PointField()

class Base(models.Model):
    name = models.CharField(max_length=32)
    gps_location = models.PointField()
    min_patrols = models.IntegerField()
    max_patrols = models.IntegerField()

class Intelligence(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    question = models.CharField(max_length=16)
    answer = models.CharField(max_length=256)

class Queue(models.Model):
    sequence = models.IntegerField()
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

class Event(models.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    check_out = models.BooleanField()
    intelligence = models.ForeignKey(Intelligence, on_delete=CASCADE)