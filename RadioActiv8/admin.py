from django.contrib.gis import admin
from .models import *

class EventAdmin(admin.ModelAdmin):
    list_display= ('timestamp', 'patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    #list_editable= ('patrol', 'location', 'intelligence_request', 'intelligence_answered_correctly', 'destination', 'comment')
    list_filter= ('patrol', 'location', 'destination')
    search_fields= ('patrol__name', 'location__radio__location_name', 'intelligence_request__answer', 'destination__radio__location_name', 'comment')

# Register your models here.
admin.site.register(Patrol, admin.OSMGeoAdmin)
admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(Radio, admin.OSMGeoAdmin)
admin.site.register(Base, admin.OSMGeoAdmin)
admin.site.register(Intelligence)
admin.site.register(Queue)
admin.site.register(Event, EventAdmin)

admin.site.site_header = "RadioActiv8 Admin"