from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('settings/', views.site_settings, name='site_settings'),
    path('upload/', views.upload_images, name='upload_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
