""" forensik URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from forensik.case import views

#Customizing "Django Admin Page" for our WebApp
admin.site.site_header = 'ForensicView'
admin.site.index_title = 'Case Manager'
admin.site.site_title = 'ForensicView Case Manager'



admin.site.site_header = 'ForensicVisualizer'
admin.site.index_title = 'Case Manager'
admin.site.site_title = 'ForensicVisualizer'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('forensik.account.urls', namespace='account')),
    path("", include('forensik.case.urls'))
]
