from django.urls import include, path
from rest_framework import routers

from . import views, api_views

router = routers.DefaultRouter()
router.register(r'bases', api_views.BaseViewSet)
router.register(r'patrols', api_views.PatrolViewSet, basename='patrol')
router.register(
    r'intelligences',
    api_views.IntelligenceViewSet,
    basename='intelligence')
router.register(
    r'patrol_answers',
    api_views.PatrolAnswerViewSet,
    basename='patrol_answer')
router.register(r'queues', api_views.QueueViewSet, basename='queue')
router.register(r'events', api_views.EventViewSet, basename='event')

app_name = 'RadioActiv8'
urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'patrol/',
        views.PatrolList.as_view(),
        name='PatrolList'),
    path(
        'patrol/<int:pk>/',
        views.PatrolDetail.as_view(),
        name='PatrolDetail'),
    path(
        'base/',
        views.BaseList.as_view(),
        name='BaseList'),
    path(
        'base/<int:pk>/',
        views.BaseDetail.as_view(),
        name='BaseDetail'),
    path('api/', include(router.urls)),
]
