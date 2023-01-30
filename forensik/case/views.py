"""Map"""
import json
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .analyze import read_images, read_csv, read_local_images
from .forms import ImageForm
from .models import Device, Geodata
from django.core.cache import cache




def analyze_data(*args):
    read_csv()
    read_images()
    response = redirect('case:map')
    return response

def get_device_folder(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('Asservat')
            directory = form.cleaned_data.get('Ordner')
            print(directory)
            read_local_images(id,directory)
            form =ImageForm()
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()
    return render(request, 'case/choose_device_directory.html', {'form': form})


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
        context["title"] = "ForensicView-Kartenansicht"
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