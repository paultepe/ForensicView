from django.contrib import admin
from .models import Case, Person, Geodata, Database,Device, Image
from django.contrib.gis import admin



@admin.register(Geodata)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""
    list_display = ("database", "date_time" , "location")

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Marker admin."""
    list_display = ("device_name","model","brand","person")

admin.site.register(Case)
admin.site.register(Database)
admin.site.register(Person)
admin.site.register(Image)

