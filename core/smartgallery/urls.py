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
    path('sys/delete_image/<int:image_id>', views.delete_image, name='delete_image'),
    path('sys/delete_all_album_images/<int:album_id>/', views.delete_all_album_images, name='delete_all_album_images'),
    path('sys/delete_album/<int:album_id>/', views.delete_album, name='delete_album'),
    path('sys/delete_all_album_hidden_images/<int:album_id>/', views.delete_all_album_hidden_images, name='delete_all_album_hidden_images'),
    path('sys/create_album/', views.create_album, name='create_album'),
    path('sys/update_image_order', views.update_image_order, name='update_image_order'),
    path('sys/update_image_name/<int:photo_id>', views.update_image_name, name='update_image_name'),
    path('sys/update_image_exif/<int:photo_id>', views.update_image_exif, name='update_image_exif'),
    path('sys/change_album/<int:photo_id>/<int:album_id>', views.change_album, name='change_album'),
    path('sys/images/<int:image_id>/change_visibility', views.change_visibility, name='change_visibility'),
    path('sys/settings', views.site_settings, name='site_settings'),
    path('sys/menu_settings', views.menu_settings, name='menu_settings'),
    path('sys/social_settings/', views.social_settings, name='social_settings'),
    path('sys/user_settings/', views.user_settings, name='user_settings'),
    path('sys/update_menu_order/', views.update_menu_order, name='update_menu_order'),
    path('sys/update_social_order/', views.update_social_order, name='update_social_order'),
    path('sys/update_menu_item_name/', views.update_menu_item_name, name='update_menu_item_name'),
    path('sys/update_social_item_name/', views.update_social_item_name, name='update_social_item_name'),
    path('sys/delete_social_item_name/<int:id>', views.delete_social_item_name, name='delete_social_item_name'),
    path('sys/delete_current_logo/', views.delete_current_logo, name='delete_current_logo'),
    path('p/timeline/', views.timeline, name='timeline'),
    path('sys/upload/', views.upload_images, name='upload_images'),
    path('sys/ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
