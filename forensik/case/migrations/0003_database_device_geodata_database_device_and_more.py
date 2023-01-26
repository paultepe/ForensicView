# Generated by Django 4.1.5 on 2023-01-25 21:50

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0002_person_case_alter_person_birthdate"),
    ]

    operations = [
        migrations.CreateModel(
            name="Database",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("database", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand", models.CharField(max_length=30)),
                ("model", models.CharField(max_length=30)),
                ("type", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Geodata",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("date_time", models.DateTimeField()),
                (
                    "database",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="case.database"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="database",
            name="device",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="case.device"
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="device",
            field=models.ManyToManyField(to="case.device"),
        ),
    ]
