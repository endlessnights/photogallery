from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<slug:album_slug>/', views.show_albums, name='show_albums'),
    path('re/<slug:album_slug>/', views.reorder_albums, name='reorder_albums'),
    path('order/update_image_order/', views.update_image_order, name='update_image_order'),
    path('back/settings/', views.site_settings, name='site_settings'),
    path('back/upload/', views.upload_images, name='upload_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
