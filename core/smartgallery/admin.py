from django.contrib import admin

# Register your models here.
from .models import Album, Image, SiteSettings


@admin.register(SiteSettings)
class Settings(admin.ModelAdmin):
    list_display = [
        'title',
        'copyright',
        'primary_color',
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Album)
class Albums(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'order',
        'status',
    ]


@admin.register(Image)
class Images(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'order',
        'image',
        'thumbnail',
        'status',
    ]
