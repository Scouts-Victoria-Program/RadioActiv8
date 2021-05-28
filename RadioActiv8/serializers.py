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
        # extra_kwargs = {
        #    'url': {'view_name': 'base-list', 'lookup_field': 'id'}
        # }


class PatrolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patrol
        fields = ['name', 'base', 'gps_location']


class IntelligenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Intelligence
        fields = ['base', 'question', 'answer']


class PatrolAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PatrolAnswer
        fields = ['patrol', 'intelligence']


class QueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Queue
        fields = ['sequence', 'base', 'patrol']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['base', 'patrol', 'timestamp', 'check_out']
