"""Map"""
import json
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .analyze import read_images, read_csv, read_local_images
from .forms import ImageForm
from .models import Device, Geodata, Case, Person
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
            device_name = form.cleaned_data.get('Asservat')
            directory = form.cleaned_data.get('Ordner')
            print(directory)
            read_local_images(device_name,directory)
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
        cases = Case.objects.all()
        for object in objects:
            if object.image_id and not object.img_url:
                object.img_url = object.get_image_url
            if object.annotation == 2 and not object.image:
                object.device_name = object.get_device_name
                object.save()
        context["cases"] = []


        for case in cases:
            case_name = case.name
            case_dict = {"name": case_name, "persons":  []}
            case_persons = Person.objects.filter(case=case)
            for person in case_persons:
                person_firstname = person.firstname
                person_lastname = person.lastname
                person_dict = {"name": person_firstname + person_lastname, "devices": []}
                person_devices = Device.objects.filter(person=person)
                for device in person_devices:
                    device_dict = {"device_name": device.device_name, "color": device.color}
                    person_dict["devices"].append(device_dict)

                case_dict["persons"].append(person_dict)

            context["cases"].append(case_dict)
        context["geodata"] = json.loads(serialize("geojson", objects))
        context["title"] = "ForensicView-Kartenansicht"
        return context