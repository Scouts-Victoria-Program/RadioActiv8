from django.db import models

# Create your models here.
class IntelligenceTuple(models.Model):
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=256)

class IntelligenceList(model.Models):
    intelligence_list = IntelligenceTuple()

class Patrol(models.Model):
    gps_location = models.CharField(max_length=100)

class Base(models.Mode):
    gps_location = models.CharField(max_length=100)
    min_patrols = models.IntegerField()
    max_patrols = models.IntegerField()

class Queue(models.Model):
    sequence = models.IntegerField()
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)

class EventType(models.TextChoices):
  CHECK_IN  = 'Check-in'
  CHECK_OUT = 'Check-out'

class Event(model.Model):
    base = models.ForeignKey(Base, on_delete=models.CASCADE)
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    event_type = EventType()
    intelligence = models.ForeignKey(IntelligenceTuple, on_delete=models.CASCADE)