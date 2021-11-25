from django.contrib.gis import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display= ('timestamp', 'patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    #list_editable= ('patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    list_filter= ('patrol', 'location', 'destination')
    search_fields= ('patrol__name', 'location__radio__location_name', 'intelligence_request__answer', 'destination__radio__location_name', 'comment')
    ordering = ['timestamp']

class PatrolAdmin(admin.OSMGeoAdmin):
    ordering = ['name']

class RadioAdmin(admin.OSMGeoAdmin):
    ordering = ['location_name']

class IntelligenceAdmin(admin.OSMGeoAdmin):
    ordering = ['base', 'question']
    list_filter= ('base',)

class LocationAdmin(admin.OSMGeoAdmin):
    ordering = ['radio__location_name']

# Register your models here.
admin.site.register(Patrol, PatrolAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Radio, RadioAdmin)
admin.site.register(Base, RadioAdmin)
admin.site.register(Intelligence, IntelligenceAdmin)
admin.site.register(Queue)
admin.site.register(Event, EventAdmin)

admin.site.site_header = "RadioActiv8 Admin"