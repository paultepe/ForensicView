"""Markers view."""
import pandas as pd
import json
import os
from pathlib import Path
from exif import Image
from forensik.case.models import Geodata
from django.contrib.gis.geos import Point
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile, File

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView

from .models import Geodata,Person,Case, Database,Image

def Frontpage(request):
    objects = Case.objects.all()
    template = loader.get_template("pages/home.html")
    context = {
        'objects': objects,
    }
    return HttpResponse(template.render(context, request))

class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "case/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        databases = Database.objects.all().filter(status=1)
        for database in databases:
            df = pd.read_csv('.'+database.file.url, sep=';')
            for index, row in df.iterrows():
                if type(row.loc['longitude']) == int and type(row.loc['latitude']) == int:
                    row.loc['longitude'] /= 10**(len(str(row.loc['longitude'])) - 2)
                    row.loc['latitude'] /= 10**(len(str(row.loc['latitude'])) - 2)
                location = Point(row.loc['longitude'], row.loc['latitude'])
                Geodata.objects.create(location=location, type=database.file, database=database )
            Database.objects.filter(pk=database.id).update(status=2)
        objects = Geodata.objects.select_related('image')
        for object in objects:
            if object.image_id and not object.img_url:
                object.img_url = object.get_image_url
                object.save()
        """
        context["data"] = {"cases": []}
        case = {
            "name":case_name,
            "geodata": json.loads(serialize("geojson", objects))
        }
        context["data"]["cases"].append(case)
        print(type(context["data"]))
       """

        context["geodata"] = json.loads(serialize("geojson", objects))
        return context