from django.contrib.gis import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display= ('timestamp', 'patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')

# Register your models here.
admin.site.register(Patrol, admin.OSMGeoAdmin)
admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(Radio, admin.OSMGeoAdmin)
admin.site.register(Base, admin.OSMGeoAdmin)
admin.site.register(Intelligence)
admin.site.register(Queue)
admin.site.register(Event, EventAdmin)
