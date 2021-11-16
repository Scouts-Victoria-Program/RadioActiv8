from rest_framework import serializers
from .models import *


class BaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Base
        fields = ['url',
                  'name',
                  'gps_location',
                  'min_patrols',
                  'max_patrols',
                  'activity_type',
                  'channel']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:base-detail'},
        }


class PatrolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patrol
        fields = ['url', 'name', 'base', 'gps_location']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:patrol-detail'},
            'base': {'view_name': 'RadioActiv8:base-detail'},
        }


class IntelligenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Intelligence
        fields = ['url', 'base', 'question', 'answer']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:intelligence-detail'},
            'base': {'view_name': 'RadioActiv8:base-detail'},
        }


class QueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Queue
        fields = ['url', 'sequence', 'base', 'patrol']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:patrol_answer-detail'},
            'base': {'view_name': 'RadioActiv8:base-detail'},
            'patrol': {'view_name': 'RadioActiv8:patrol-detail'},
        }


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'base', 'patrol', 'timestamp', 'check_out']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:event-detail'},
            'base': {'view_name': 'RadioActiv8:base-detail'},
            'patrol': {'view_name': 'RadioActiv8:patrol-detail'},
        }
