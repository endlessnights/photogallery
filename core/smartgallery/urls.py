from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('<slug:album_slug>/', views.show_albums, name='show_albums'),
    path('re/<slug:album_slug>', views.reorder_albums, name='reorder_albums'),
    path('order/update_image_order', views.update_image_order, name='update_image_order'),
    path('order/update_image_name/<int:photo_id>', views.update_image_name, name='update_image_name'),
    path('order/change_album/<int:photo_id>/<int:album_id>', views.change_album, name='change_album'),
    path('order/images/<int:image_id>/change_visibility', views.change_visibility, name='change_visibility'),
    path('back/settings/', views.site_settings, name='site_settings'),
    path('back/upload/', views.upload_images, name='upload_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
