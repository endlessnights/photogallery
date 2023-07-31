from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.utils import timezone
from .models import Album, MenuItem, SiteSettings


@receiver(post_save, sender=Album)
def create_menu_item(sender, instance, created, **kwargs):
    if created:
        MenuItem.objects.create(album=instance, name=instance.name)


@receiver(post_migrate)
def create_initial_site_settings(sender, **kwargs):
    if sender.name == 'smartgallery':  # Replace 'your_app_name' with the actual name of your Django app
        if not SiteSettings.objects.exists():
            default_settings = SiteSettings(
                title='Smart Photo Gallery',
            )
            default_settings.save()