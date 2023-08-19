from django.contrib import admin

# Register your models here.
from .models import Album, Image, SiteSettings, MenuItem, SocialLinks


@admin.register(SiteSettings)
class Settings(admin.ModelAdmin):
    list_display = [
        'title',
        'copyright',
        'topbar_bgcolor',
    ]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


# @admin.register(AboutPage)
# class IndexPage(admin.ModelAdmin):
#     list_display = [
#         'name',
#     ]
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request):
#         return not AboutPage.objects.exists()


@admin.register(SocialLinks)
class SocialLinks(admin.ModelAdmin):
    list_display = [
        'name',
        'link',
        'icon',
        'order',
    ]

@admin.register(Album)
class Albums(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'order',
        'status',
    ]


@admin.register(MenuItem)
class MenuItems(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'album',
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
