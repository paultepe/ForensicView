"""Markers urls."""

from django.urls import path

from . import views

app_name = "case"

urlpatterns = [
    path("map/", views.MarkersMapView.as_view(), name='map'),
    path("", views.Frontpage)
]