from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers

from . import api_views, views

router = routers.DefaultRouter()
router.register(r"base", api_views.BaseViewSet)
router.register(r"patrol", api_views.PatrolViewSet, basename="patrol")
router.register(r"intelligence", api_views.IntelligenceViewSet, basename="intelligence")
router.register(r"event", api_views.EventViewSet, basename="event")

app_name = "RadioActiv8"
urlpatterns = [
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    path("", views.index, name="index"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="RadioActiv8/user_auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="RadioActiv8/user_auth/login.html"),
        name="logout",
    ),
    path("play/", views.play, name="play"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("patrol_locations/", views.patrol_locations, name="patrol_locations"),
    path("map/", views.map, name="map"),
    path("lab/", views.participant_homepage, name="participant_homepage"),
    path(
        "lab/patrol/<int:pk>", views.participant_base_list, name="participant_base_list"
    ),
    path(
        "lab/patrol/<int:patrol_pk>/base/<int:base_pk>",
        views.participant_base_detail,
        name="participant_base_detail",
    ),
    path("patrol/", views.PatrolList.as_view(), name="PatrolList"),
    path("patrol/<int:pk>/", views.PatrolDetail, name="PatrolDetail"),
    path("base/", views.BaseList.as_view(), name="BaseList"),
    path("base/<int:pk>/", views.BaseDetail.as_view(), name="BaseDetail"),
    path("base_test/<int:base_id>/", views.base_test, name="base_test"),
    path("event_ajax", views.event_ajax, name="event_ajax"),
    path("event/", views.EventList, name="EventList"),
    path("event/create", views.EventCreate.as_view(), name="EventCreate"),
    path("bases_geojson", views.bases_geojson, name="bases_geojson"),
    path("session/", views.SessionList.as_view(), name="SessionList"),
    path("session/set", views.SetWorkingSession, name="SetWorkingSession"),
    path("session/current", views.CurrentSessionDetail, name="CurrentSessionDetail"),
    path(
        "session/current/<path:path>",
        views.CurrentSessionDetail,
        name="CurrentSessionDetail",
    ),
    path("session/<int:pk>/", views.SessionDetail.as_view(), name="SessionDetail"),
    path(
        "session/<int:pk>/patrol/",
        views.SessionDetail.as_view(
            template_name="RadioActiv8/session/patrol_index.html"
        ),
        name="SessionPatrolList",
    ),
    path("session/<int:pk>/clock/", views.SessionClock, name="SessionClock"),
    path(
        "session/<int:pk>/base/",
        views.SessionDetail.as_view(
            template_name="RadioActiv8/session/base_index.html"
        ),
        name="SessionBaseList",
    ),
    path(
        "session/<int:pk>/patrol/add",
        views.add_patrol_to_session,
        name="SessionAddPatrol",
    ),
    path("gpstracker/", views.GPSTrackerList, name="GPSTrackerList"),
    path("gpstracker/<int:pk>/", views.GPSTrackerDetail, name="GPSTrackerDetail"),
    path("api/", include(router.urls)),
]
