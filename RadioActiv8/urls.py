from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views, api_views

router = routers.DefaultRouter()
router.register(r'base', api_views.BaseViewSet)
router.register(r'patrol', api_views.PatrolViewSet, basename='patrol')
router.register(
    r'intelligence',
    api_views.IntelligenceViewSet,
    basename='intelligence')
router.register(r'event', api_views.EventViewSet, basename='event')

app_name = 'RadioActiv8'
urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='user_auth/login.html'),
        name='login'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='user_auth/login.html'),
        name='logout'),
    path(
        'play/',
        views.play,
        name='play'),
    path(
        'map/',
        views.map,
        name='map'),
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
    path(
        'base_test/<int:base_id>/',
        views.base_test,
        name='base_test'),
    path(
        'event_ajax',
        views.event_ajax,
        name='event_ajax'),
    path(
        'event/',
        views.EventList,
        name='EventList'),
    path(
        'event/create',
        views.EventCreate.as_view(),
        name='EventCreate'),
    path(
        'bases_geojson',
        views.bases_geojson,
        name='bases_geojson'),
    path(
        'session/',
        views.SessionList.as_view(),
        name='SessionList'),
    path(
        'session/<int:pk>/',
        views.SessionDetail.as_view(),
        name='SessionDetail'),
    path(
        'session/<int:pk>/patrol/',
        views.SessionDetail.as_view(template_name='session/patrol_index.html'),
        name='SessionPatrolList'),
    path(
        'session/<int:pk>/base/',
        views.SessionDetail.as_view(template_name='session/base_index.html'),
        name='SessionBaseList'),
    path('api/', include(router.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# FIXME: Serve static files properly in production
