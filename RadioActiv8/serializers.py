from rest_framework import serializers
from .models import *


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['url',
                  'gps_location']
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


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'timestamp', 'location', 'patrol', 'comment', 'destination', 'intelligence_request', 'intelligence_answered_correctly']
        extra_kwargs = {
            'url': {'view_name': 'RadioActiv8:event-detail'},
            'location': {'view_name': 'RadioActiv8:location-detail'},
            'patrol': {'view_name': 'RadioActiv8:patrol-detail'},
            'destination': {'view_name': 'RadioActiv8:location-detail'},
        }
