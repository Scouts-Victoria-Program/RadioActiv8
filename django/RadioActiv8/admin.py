from django.contrib.gis import admin
from .models import (
    Patrol,
    Location,
    Radio,
    Base,
    Intelligence,
    Event,
    Session,
    GPSTracker,
)

from RadioActiv8.forms import EventForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import csv
from simple_history.admin import SimpleHistoryAdmin


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


class EventAdmin(SimpleHistoryAdmin):
    list_display = (
        "timestamp",
        "session",
        "patrol",
        "location",
        "intelligence_request",
        "intelligence_answered_correctly",
        "destination",
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
    ordering = ["timestamp"]
    form = EventForm


class PatrolAdmin(SimpleHistoryAdmin):
    search_fields = ("name",)
    list_filter = ("session",)


class RadioAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    list_filter = ("session",)


class IntelligenceAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    list_filter = ("base",)


class LocationAdmin(SimpleHistoryAdmin, admin.GISModelAdmin):
    ordering = ["radio__name"]


class SessionAdmin(SimpleHistoryAdmin):
    pass


class GPSTrackerAdmin(SimpleHistoryAdmin):
    pass


# Register your models here.
admin.site.register(Patrol, PatrolAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Radio, RadioAdmin)
admin.site.register(Base, RadioAdmin)
admin.site.register(Intelligence, IntelligenceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(GPSTracker, GPSTrackerAdmin)

# admin.site.site_header = "RadioActiv8 Admin"
