import csv

from simple_history.admin import SimpleHistoryAdmin

from django.contrib.gis import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from RadioActiv8.forms import EventForm

from .models import (
    Base,
    BaseRoutePair,
    Event,
    GPSTracker,
    Intelligence,
    Location,
    Patrol,
    Radio,
    Session,
)


@admin.action(description="Download selected as csv")
def download_csv(modeladmin, request, queryset):
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    # model = queryset.model
    response = HttpResponse(content_type="text/csv")
    # force download.
    response["Content-Disposition"] = "attachment;filename=export.csv"
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


admin.site.add_action(download_csv, "download_csv")


@admin.register(Event)
class EventAdmin(SimpleHistoryAdmin):
    list_display = (
        "timestamp",
        "timesince",
        "patrol",
        "location",
        "destination",
        "intelligence_request",
        "intelligence_answered_correctly",
        "session",
        "comment",
    )
    # list_editable= ('patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    list_filter = ("patrol", "location", "destination", "session")
    search_fields = (
        "patrol__name",
        "location__radio__name",
        "intelligence_request__answer",
        "destination__radio__name",
        "comment",
    )
    ordering = ["-timestamp"]
    form = EventForm


# @admin.register(Participant)
class ParticipantAdmin(SimpleHistoryAdmin):
    search_fields = ("full_name", "p_id", "patrol__name")


@admin.register(Patrol)
class PatrolAdmin(SimpleHistoryAdmin):
    search_fields = ("name",)
    list_filter = ("session",)


class EventPatrolInline(admin.TabularInline):
    model = Intelligence
    readonly_fields = []
    fields = [
        "question",
        "answer",
        "completion_points",
    ]
    show_change_link = True


@admin.register(Base)
class BaseAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    list_filter = ("session",)
    search_fields = (
        "name",
        "description",
    )
    list_display = (
        "name",
        "description",
        "channel",
        "min_patrols",
        "max_patrols",
        "get_patrols_count",
        "is_full",
        "repeatable",
        "attendance_points",
        "activity_type",
    )
    list_editable = (
        "description",
        "channel",
        "min_patrols",
        "max_patrols",
        "repeatable",
        "attendance_points",
        "activity_type",
    )
    autocomplete_fields = ("session",)
    inlines = (EventPatrolInline,)


@admin.register(Radio)
class RadioAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    list_filter = ("session",)


@admin.register(Intelligence)
class IntelligenceAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    list_filter = ("base",)


@admin.register(Location)
class LocationAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    ordering = ["radio__name"]


@admin.register(Session)
class SessionAdmin(SimpleHistoryAdmin):
    search_fields = ("name",)


@admin.register(GPSTracker)
class GPSTrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseRoutePair)
class BaseRoutePairAdmin(admin.ModelAdmin):
    list_display = (
        "source",
        "destination",
        "time",
        "length",
    )
    search_fields = (
        "source",
        "destination",
    )
    list_filter = ("source",)


# admin.site.site_header = "RadioActiv8 Admin"
