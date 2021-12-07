from rest_framework import viewsets, permissions
from .serializers import *
from .models import *


class BaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bases to be viewed or edited.
    """
    queryset = Base.objects.all()
    serializer_class = BaseSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatrolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patrols to be viewed or edited.
    """
    queryset = Patrol.objects.all()
    serializer_class = PatrolSerializer
    permission_classes = [permissions.IsAuthenticated]


class IntelligenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows intelligences to be viewed or edited.
    """
    queryset = Intelligence.objects.all()
    serializer_class = IntelligenceSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
