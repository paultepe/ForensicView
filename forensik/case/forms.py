from django.forms import forms
from forensik.case.models import Device
from django import forms

class NameForm(forms.Form):
    CHOICES = []
    devices = Device.objects.values('device_name', 'color').distinct()
    for device in devices:
        CHOICES.append((1, device['device_name']))
    geraet = forms.ChoiceField(choices=CHOICES)

