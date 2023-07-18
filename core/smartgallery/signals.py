from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Album, MenuItem


@receiver(post_save, sender=Album)
def create_menu_item(sender, instance, created, **kwargs):
    if created:
        MenuItem.objects.create(album=instance, name=instance.name)
