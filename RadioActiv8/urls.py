from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'RadioActiv8'
urlpatterns = [
    path(
        '',
        views.index,
        name='index'),
    path(
        'login/',
        views.login,
        name='login'),
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
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# FIXME: Serve static files properly in production
