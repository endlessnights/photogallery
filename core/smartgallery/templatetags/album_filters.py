from django import template
import random

register = template.Library()


@register.filter(name='album')
def filter_images_by_album(images, album_slug, limit=None):
    filtered_images = images.filter(album__slug=album_slug)

    if limit is not None:
        try:
            limit = int(limit)
            if limit > 0:
                filtered_images = filtered_images[:limit]
        except ValueError:
            pass  # Handle invalid limit value

    return filtered_images
