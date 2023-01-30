from django.contrib.gis.db.models import PointField
from colorfield.fields import ColorField
from django.db import models
from django.utils.safestring import mark_safe

STATUS = ((1, 'Nicht analysiert'),(2, 'Analysiert'))

# Create your models here.
class Case(models.Model):
    name = models.CharField(max_length=50)
    case_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Annotation(models.Model):
    case = models.ForeignKey(to=Case, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Person(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    birthdate = models.DateField()
    case = models.ManyToManyField(Case)

    def __str__(self):
        return self.firstname +" "+ self.lastname

class Device(models.Model):
    device_name = models.CharField(max_length=40)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    person = models.ForeignKey(to=Person, on_delete=models.CASCADE)
    color = ColorField()
    image_import = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.device_name

    def get_device(self):
        return (self.id,self.device_name)

class Database(models.Model):
    database = models.CharField(max_length=30)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    file = models.FileField(upload_to='databases')
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.database
2
class Image(models.Model):
    image = models.FileField(upload_to='images',blank=True, null=True )
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE,blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.image.name

    def image_name(self):
        return self.image.name

    def show_image(self):  # new
        return mark_safe(f'<img src = "{self.image.url}" width = "300"/>')


class Geodata(models.Model):
    location = PointField()
    date_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=30)
    database = models.ForeignKey(to=Database, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(to=Image, on_delete=models.CASCADE, blank=True, null=True)
    img_url = models.CharField(max_length=100,blank=True, null=True)
    device_name = models.CharField(max_length=50, blank=True, null=True)
    annotation = models.ForeignKey(to=Annotation, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return str(self.location.coords)

    @property
    def get_image_url(self):
      img = Image.objects.get(id=self.image.pk)
      img_url = img.image.url
      return img_url

    @property
    def get_device_name(self):
      device = Device.objects.get(database=self.database)
      return device.device_name
