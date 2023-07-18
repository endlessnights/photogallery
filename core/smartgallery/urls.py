from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path(r'(?P<album>[a-zA-Z0-9]+)/$', views.ShowAlbum, name='album'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
