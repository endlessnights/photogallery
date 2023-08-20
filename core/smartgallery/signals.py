from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from .models import Album, MenuItem, SiteSettings


@receiver(post_save, sender=Album)
def create_menu_item(sender, instance, created, **kwargs):
    if created:
        MenuItem.objects.create(album=instance, name=instance.name)


@receiver(post_migrate)
def create_initial_site_settings(sender, **kwargs):
    if sender.name == 'smartgallery':
        if not SiteSettings.objects.exists():
            default_settings = SiteSettings(
                title='Smart Photo Gallery',
            )
            try:
                index_template = get_template('front/demo/index.html')
                default_settings.index_content = index_template.render()
            except FileNotFoundError:
                error_msg = "Template file '/front/demo/index.html' not found. Default content not set."
                print(error_msg)
            try:
                about_template = get_template('front/demo/about_me.html')
                default_settings.index_content = about_template.render()
            except FileNotFoundError:
                error_msg = "Template file '/front/demo/about_me.html' not found. Default content not set."
                print(error_msg)
            default_settings.save()


@receiver(post_migrate)
def create_demo_user(sender, **kwargs):
    if sender.name == 'smartgallery':  # Replace 'your_app_name' with the actual name of your Django app
        UserModel = get_user_model()
        if not UserModel.objects.filter(username='demo').exists():
            demo_user = UserModel.objects.create_user(
                username='root',
                password='RootPassword',  # You can set any default password here
                email='demo@example.com',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            demo_user.save()