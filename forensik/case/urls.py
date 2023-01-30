from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "case"


urlpatterns = [
    path("", views.MapView.as_view(), name='map'),
    path("analyse", views.analyze_data, name='analyze'),
    path("image_import", views.get_device_folder, name='image_import')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)