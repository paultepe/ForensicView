
import os
from datetime import datetime

from django.core.files.base import File
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
    databases = Database.objects.all()
    for database in databases:
        df = pd.read_csv('.' + database.file.url, sep=';',encoding = "ISO-8859-1",error_bad_lines=False)
        for index, row in df.iterrows():
            if type(row.loc['longitude']) == int and type(row.loc['latitude']) == int:
                row.loc['longitude'] /= 10 ** (len(str(row.loc['longitude'])) - 2)
                row.loc['latitude'] /= 10 ** (len(str(row.loc['latitude'])) - 2)
            location = Point(row.loc['longitude'], row.loc['latitude'])
            date = timestamp_to_data(row.loc['timestamp'])
            Geodata.objects.create(location=location, type=database.file, database=database,date_time=date, annotation=2)
        Database.objects.filter(pk=database.id).update(status=2)


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

def timestamp_to_data(timestamp):
    if len(str(timestamp)) == 13:
        timestamp /= 1000
    print(timestamp)
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object

def read_images():
    images = Image.objects.all().filter(status=1)
    for image in images:
        coords,date = image_coordinates('.' + image.image.url)
        point = Point(coords)
        if (point and date):
            Geodata.objects.create(location=point, type="image", image=image, device_name=image.device.device_name, date_time=date)
        image.status = 2
        image.save()


def read_local_images(device,directory):
    device_object = Device.objects.get(id=device)
    if device_object.image_import == 2:
        return ("Bereits importiert")
    filepaths = get_image_paths("./user_data/images/"+directory)
    print(filepaths)
    for file in filepaths:
        coords,date = image_coordinates(file)
        with open(file, 'rb') as f:
            if coords and date:
                point = Point(coords)
                image_object = Image.objects.create(image=(File(f)),status=2,device=device_object)
                Geodata.objects.create(location=point, type="image",date_time=date, image=image_object, annotation=2,device_name=device_object.device_name)
    device_object.image_import = 2
    device_object.save()