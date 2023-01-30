"""Map"""
import os
from .helper import read_images,read_csv,read_local_images
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm
import pandas as pd
import json
from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import Geodata, Database, Device,Image
from exif import Image as ExifImage
from forensik.case.models import Geodata
from django.contrib.gis.geos import Point



def analyze_data(*args):
    read_csv()
    read_images()
    response = redirect('case:map')
    return response

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('geraet')
            read_local_images(id)
            return HttpResponseRedirect('/')
            HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'case/submit_to_analyze.html', {'form': form})

class MapView(TemplateView):
    """Markers map view."""

    template_name = "case/map.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        objects = Geodata.objects.all()
        for object in objects:
            if object.image_id and not object.img_url:
                object.img_url = object.get_image_url
            if object.annotation == 2 and not object.image:
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