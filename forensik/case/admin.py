from django.contrib import admin
from .models import Case, Person, Geodata, Database, Device, Image
from django.contrib.gis import admin


@admin.register(Geodata)
class MarkerAdmin(admin.OSMGeoAdmin):
    'Marker admin.'
    fields = ('location', 'device_name', 'date_time', 'type', 'database', 'image')
    readonly_fields = ('database', 'device_name')
    list_display = ('database', 'date_time', 'location')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'model', 'brand', 'person')
    readonly_fields = ('image_import',)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'case_type')


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('database','device','file','status')
    readonly_fields = ('status',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display =('lastname','firstname','birthdate')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_name','device','status')
    readonly_fields = ('show_image','status')



