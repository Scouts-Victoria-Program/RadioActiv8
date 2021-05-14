from django.urls import path

from . import views

app_name = 'RadioActiv8'
urlpatterns = [
        path('', views.index, name='index'),
        path('patrol/', views.PatrolList.as_view(), name='PatrolList'),
        path('patrol/<int:pk>/', views.PatrolDetail.as_view(), name='PatrolDetail'),
        path('base/', views.BaseList.as_view(), name='BaseList'),
        path('base/<int:pk>/', views.BaseDetail.as_view(), name='BaseDetail'),
        ]
