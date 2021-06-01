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
router.register(
    r'patrol_answer',
    api_views.PatrolAnswerViewSet,
    basename='patrol_answer')
router.register(r'queue', api_views.QueueViewSet, basename='queue')
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
    path('api/', include(router.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# FIXME: Serve static files properly in production
