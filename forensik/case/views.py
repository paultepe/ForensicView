"""Map"""
import os

import pandas as pd
import json
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import Geodata, Database, Device,Image
from exif import Image as ExifImage
from forensik.case.models import Geodata
from django.contrib.gis.geos import Point



def analyze_data(*args):
    def read_csv():
        """Return the view context data."""
        databases = Database.objects.all().filter(status=1)
        for database in databases:
            df = pd.read_csv('.' + database.file.url, sep=';')
            for index, row in df.iterrows():
                if type(row.loc['longitude']) == int and type(row.loc['latitude']) == int:
                    row.loc['longitude'] /= 10 ** (len(str(row.loc['longitude'])) - 2)
                    row.loc['latitude'] /= 10 ** (len(str(row.loc['latitude'])) - 2)
                location = Point(row.loc['longitude'], row.loc['latitude'])
                Geodata.objects.create(location=location, type=database.file, database=database, annotation=2)
            Database.objects.filter(pk=database.id).update(status=2)


    def read_images():
        def decimal_coords(coords, ref):
            decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
            if ref == "S" or ref == 'W':
                decimal_degrees = -decimal_degrees
            return decimal_degrees
        def image_coordinates(image_path):
            with open(image_path, 'rb') as src:
                img = ExifImage(src)
            if img.has_exif:
                try:
                    coords = (decimal_coords(img.gps_longitude,
                                             img.gps_longitude_ref),
                              decimal_coords(img.gps_latitude,
                                             img.gps_latitude_ref))
                except AttributeError:
                    return
                return coords

        images = Image.objects.all().filter(status=1)
        for image in images:
            coords = image_coordinates('.'+image.image.url)
            point = Point(coords)
            print(point)
            if (point):
                Geodata.objects.create(location=point, type="image", image=image, device_name=image.device.device_name)
            image.status = 2
            image.save()
    read_csv()
    read_images()
    response = redirect('case:map')
    return response



class MapView(TemplateView):
    """Markers map view."""

    template_name = "case/map.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        objects = Geodata.objects.all()
        for object in objects:
            if object.image_id and not object.img_url:
                object.img_url = object.get_image_url
            if object.annotation == 2:
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


"""


context["cases"] = [
    {"name":"",
     "persons":
         [
             {
                 "name":"",
                 "devices":
              [
                  {
                      "device_name":"",
                      "color":""
                  }
              ]
          }
     ],
     "annotations":""
     }]

1 For-loop -> case
    2. Pers
        3 device

"""