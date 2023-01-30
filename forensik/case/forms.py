import os
from forensik.settings import BASE_DIR
from django import forms
from forensik.case.models import Device



class ImageForm(forms.Form):
    CHOICES = []
    DIRECTORY = []
    for folder in os.listdir(BASE_DIR /'user_data/images'):
        if os.path.isdir(os.path.join(BASE_DIR /'user_data/images', folder)):
            DIRECTORY.append((folder,folder))
    devices = Device.objects.values('device_name').distinct()
    for device in devices:
        obj = Device.objects.get(device_name=device['device_name'])
        CHOICES.append((obj.pk, device['device_name']))

    Asservat = forms.ChoiceField(choices=CHOICES)
    Ordner = forms.ChoiceField(choices=DIRECTORY)
