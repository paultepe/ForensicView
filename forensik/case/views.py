"""Map"""

import pandas as pd
import json
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.views.generic.base import TemplateView
from .models import Geodata, Database, Device


class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "case/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        databases = Database.objects.all().filter(status=1)
        for database in databases:
            df = pd.read_csv('.' + database.file.url, sep=';')
            for index, row in df.iterrows():
                if type(row.loc['longitude']) == int and type(row.loc['latitude']) == int:
                    row.loc['longitude'] /= 10 ** (len(str(row.loc['longitude'])) - 2)
                    row.loc['latitude'] /= 10 ** (len(str(row.loc['latitude'])) - 2)
                location = Point(row.loc['longitude'], row.loc['latitude'])
                Geodata.objects.create(location=location, type=database.file, database=database)
            Database.objects.filter(pk=database.id).update(status=2)
        objects = Geodata.objects.select_related('image')
        for object in objects:
            if object.image_id and not object.img_url:
                object.img_url = object.get_image_url
            object.device_name = object.get_device_name
            object.save()
        context["devices"] = []

        device_names = Device.objects.values('device_name', 'color').distinct()
        for device in device_names:
            context["devices"].append({"device_name": device["device_name"],
                                       "color": device['color']})
        context["geodata"] = json.loads(serialize("geojson", objects))
        print(context["geodata"])
        return context
