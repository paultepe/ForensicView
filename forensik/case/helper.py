import os
import os
from pathlib import Path
from exif import Image as ExifImage
from forensik.case.models import Geodata, Image
from django.contrib.gis.geos import Point
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile, File

import pandas as pd
from pathlib import Path
from .models import Geodata, Database, Device,Image
from exif import Image as ExifImage
from forensik.case.models import Geodata
from django.contrib.gis.geos import Point

def get_image_paths(directory):
    image_extensions = ['.jpg', '.jpeg']
    image_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if Path(file_path).suffix.lower() in image_extensions:
                image_paths.append(file_path)
    return image_paths

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


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = ExifImage(src)
        print(img.list_all())
    if img.has_exif:
        try:
            date = format_date(img.datetime)
            coords = (decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref),
                            decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref))

        except AttributeError:
            return
        return coords,date

def format_date(date_str):
    date, time = date_str.split(" ")
    year, month, day = date.split(":")
    hour, minute, second = time.split(":")
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def read_images():
    images = Image.objects.all().filter(status=1)
    for image in images:
        coords = image_coordinates('.' + image.image.url)
        point = Point(coords)
        print(point)
        if (point):
            Geodata.objects.create(location=point, type="image", image=image, device_name=image.device.device_name)
        image.status = 2
        image.save()


def read_local_images(device):
    filepaths = get_image_paths("./user_data")
    for file in filepaths:
        print(file)
        coords,date = image_coordinates(file)
        print(coords)
        with open(file, 'rb') as f:
            if coords and date:
                print(coords)
                point = Point(coords)
                print(coords,date)
                device_object = Device.objects.get(id=device)
                image_object = Image.objects.create(image=(File(f)),status=2,device=device_object)
                Geodata.objects.create(location=point, type="image",date_time=date, image=image_object, annotation=2,device_name=device_object.device_name)
