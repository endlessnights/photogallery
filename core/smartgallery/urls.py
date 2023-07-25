from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('p/about/', views.about, name='about'),
    path('sys/edit_about/', views.edit_about, name='edit_about'),
    path('<slug:album_slug>/', views.show_albums, name='show_albums'),
    path('sys/<int:album_id>', views.edit_album, name='edit_album'),
    path('sys/create_album/', views.create_album, name='create_album'),
    path('sys/update_image_order', views.update_image_order, name='update_image_order'),
    path('sys/update_image_name/<int:photo_id>', views.update_image_name, name='update_image_name'),
    path('sys/change_album/<int:photo_id>/<int:album_id>', views.change_album, name='change_album'),
    path('sys/images/<int:image_id>/change_visibility', views.change_visibility, name='change_visibility'),
    path('sys/settings', views.site_settings, name='site_settings'),
    path('sys/update_menu_order/', views.update_menu_order, name='update_menu_order'),
    path('sys/update_menu_item_name/', views.update_menu_item_name, name='update_menu_item_name'),
    path('sys/add_social/', views.add_social, name='add_social'),
    path('sys/upload/', views.upload_images, name='upload_images'),
    path('sys/ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
