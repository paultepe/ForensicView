import os
import random
from pathlib import Path
from exif import Image
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

def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_longitude,
                                     img.gps_longitude_ref),
                            decimal_coords(img.gps_latitude,
                                     img.gps_latitude_ref))

        except AttributeError:
            return
        return coords



filepaths = get_image_paths("./data/static/to_analyze")
for file in filepaths:
    coords = image_coordinates(file)
    print(file)
    if coords:
        point = Point(coords)
        obj = Geodata(location=point, type="image")
        obj.save()
