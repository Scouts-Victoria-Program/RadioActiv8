from django.contrib.gis import admin
from .models import *
from RadioActiv8.forms import EventForm

class EventAdmin(admin.ModelAdmin):
    list_display= ('timestamp', 'session', 'patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    #list_editable= ('patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    list_filter= ('patrol', 'location', 'destination', 'session')
    search_fields= ('patrol__name', 'location__radio__name', 'intelligence_request__answer', 'destination__radio__name', 'comment')
    ordering = ['timestamp']
    form = EventForm

class ParticipantAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'p_id', 'patrol__name')

class PatrolAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter= ('session',)

class RadioAdmin(admin.OSMGeoAdmin):
    list_filter= ('session',)

class IntelligenceAdmin(admin.OSMGeoAdmin):
    list_filter= ('base',)

class LocationAdmin(admin.OSMGeoAdmin):
    ordering = ['radio__name']

class SessionAdmin(admin.ModelAdmin):
    pass

class GPSTrackerAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Patrol, PatrolAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Radio, RadioAdmin)
admin.site.register(Base, RadioAdmin)
admin.site.register(Intelligence, IntelligenceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(GPSTracker, GPSTrackerAdmin)

admin.site.site_header = "RadioActiv8 Admin"