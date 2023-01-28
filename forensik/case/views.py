"""Markers view."""

import json

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView

from .models import Geodata,Person,Case

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
        objects = Geodata.objects.all()
        for object in objects:
            print(object.image)
            object.image = object.popupContent
        context["geodata"] = json.loads(serialize("geojson", objects))
        return context