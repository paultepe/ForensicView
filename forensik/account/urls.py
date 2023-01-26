# account/urls.py
from . import views
from django.urls import path

app_name = "account"

urlpatterns = [
    path("signup/", views.registerpage, name='signup'),
]