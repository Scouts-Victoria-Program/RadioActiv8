from rest_framework import viewsets, permissions
from .serializers import *
from .models import *


class BaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bases to be viewed or edited.
    """
    queryset = Base.objects.all()
    serializer_class = BaseSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PatrolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patrols to be viewed or edited.
    """
    queryset = Patrol.objects.all()
    serializer_class = PatrolSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IntelligenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows intelligences to be viewed or edited.
    """
    queryset = Intelligence.objects.all()
    serializer_class = IntelligenceSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PatrolAnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patrol_answers to be viewed or edited.
    """
    queryset = PatrolAnswer.objects.all()
    serializer_class = PatrolAnswerSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QueueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows queues to be viewed or edited.
    """
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # FIXME: tighten read permissions on these views
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
