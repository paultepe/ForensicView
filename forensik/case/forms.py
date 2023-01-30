import os
from forensik.settings import BASE_DIR
from django import forms
from forensik.case.models import Device



class ImageForm(forms.Form):
    DIRECTORY = []
    for folder in os.listdir(BASE_DIR /'user_data/images'):
        if os.path.isdir(os.path.join(BASE_DIR /'user_data/images', folder)):
            DIRECTORY.append((folder,folder))
    devices = Device.objects.values('device_name').distinct()

    Asservat = forms.CharField(max_length=50)
    Ordner = forms.ChoiceField(choices=DIRECTORY)
