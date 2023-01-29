from django.contrib.gis.db.models import PointField
from django.db import models


STATUS = ((1, 'Nicht analysiert'),(2, 'Analysiert'))

# Create your models here.
class Case(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Device(models.Model):
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.model


class Person(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    birthdate = models.DateField()
    case = models.ManyToManyField(Case)
    device = models.ManyToManyField(Device)

    def __str__(self):
        return self.firstname +" "+ self.lastname

class Database(models.Model):
    database = models.CharField(max_length=30)
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    file = models.FileField(upload_to='databases',blank=True, null=True )
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.database

class Image(models.Model):
    image = models.FileField(upload_to='images',blank=True, null=True )
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=1)

    def __str__(self):
        return self.image.name


class Geodata(models.Model):
    location = PointField()
    date_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True )
    database = models.ForeignKey(to=Database, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(to=Image, on_delete=models.CASCADE, blank=True, null=True)
    img_url = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return str(self.location.coords)
    @property
    def get_image_url(self):
      img = Image.objects.get(id=self.image.pk)
      img_url = img.image.url
      return img_url
