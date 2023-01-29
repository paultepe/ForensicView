from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "case"

urlpatterns = [
    path("", views.MarkersMapView.as_view(), name='map')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)