from django.contrib import admin

# Register your models here.
from .models import Album, Image


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
        'name',
        'order',
        'status',
    ]