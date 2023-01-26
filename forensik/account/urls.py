# account/urls.py
from . import views
from django.urls import path

urlpatterns = [
    path("signup/", views.registerpage, name="signup"),
]