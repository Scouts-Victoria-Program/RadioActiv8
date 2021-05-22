from django.contrib.gis import admin
from .models import *

# Register your models here.
admin.site.register(Patrol, admin.OSMGeoAdmin)
admin.site.register(Base, admin.OSMGeoAdmin)
admin.site.register(Intelligence)
admin.site.register(PatrolAnswer)
admin.site.register(Queue)
admin.site.register(Event)
