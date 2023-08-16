from django.apps import AppConfig


class SmartgalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smartgallery'
    verbose_name = 'SmartGallery CRM'

    def ready(self):
        from . import signals
