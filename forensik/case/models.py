from django.contrib.gis.db.models import PointField
from django.db import models


# Create your models here.
class Case(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Device(models.Model):
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


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

class Geodata(models.Model):
    location = PointField()
    date_time = models.DateTimeField()
    database = models.ForeignKey(to=Database, on_delete=models.CASCADE, blank=True, null=True)

