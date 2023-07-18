import datetime
import os
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class SiteSettings(models.Model):
    title = models.CharField(verbose_name='Website title', max_length=100, blank=True, default='Smart Photo Gallery')
    primary_color = models.CharField(verbose_name='Primary color', max_length=8, default="#007bff")
    copyright = models.CharField(
        verbose_name='Copyright text',
        max_length=1000,
        blank=True,
        default=f'Smart Photo Gallery - {datetime.datetime.now().year}'
    )
    menu_delimiter = models.CharField(verbose_name='Menu delimiter', max_length=5, blank=True, default=' | ')
    title_delimiter = models.CharField(verbose_name='Title delimiter', max_length=5, blank=True, default=' · ')

    def __str__(self):
        return self.title


class Album(models.Model):
    slug = models.CharField(verbose_name='SLUG', max_length=128, blank=False, null=False)
    name = models.CharField(verbose_name='Album name', max_length=128, blank=False, null=False)
    desc = models.TextField(verbose_name='About album', max_length=2000, blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name='Order', blank=True)
    status = models.BooleanField(verbose_name='Visibility', default=True)
    cover = models.ImageField(upload_to='album_covers', blank=True, null=True)

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


def image_path(instance, filename):
    # instance.album.slug contains the name of the Album
    # filename contains the original filename of the uploaded image
    return os.path.join('image', instance.album.slug, filename)


def thumbnail_path(instance, filename):
    # instance.album.slug contains the name of the Album
    # filename contains the original filename of the uploaded image
    return os.path.join('thumbnails', instance.album.slug, filename)


class Image(models.Model):
    name = models.CharField(verbose_name='Image name', max_length=250, blank=True)
    image = models.ImageField(upload_to=image_path)
    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True, null=True)
    album = models.ForeignKey(Album,
                              on_delete=models.PROTECT,
                              verbose_name='Choose Album')
    order = models.PositiveIntegerField(verbose_name='Order', blank=True, default=0)
    status = models.BooleanField(verbose_name='Visibility', default=True)

    def resize_and_crop(self, size):
        # Open the original image using PIL
        pil_image = PILImage.open(self.image.path)

        # if pil_image.mode == 'RGBA':
        #     pil_image = pil_image.convert('RGB')

        # Get the size of the original image
        width, height = pil_image.size

        # Calculate the scale factor for zooming
        scale_factor = max(size[0] / width, size[1] / height)

        # Calculate the new size after zooming
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Resize the image using the calculated scale factor
        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

        # Calculate the crop box to cover the target size
        left = (new_width - size[0]) / 2
        top = (new_height - size[1]) / 2
        right = left + size[0]
        bottom = top + size[1]

        # Crop the image to cover the target size
        cropped_image = pil_image.crop((left, top, right, bottom))

        # Set the image quality (adjust this as needed, 0-100)
        image_quality = 80

        # Create a BytesIO object to store the resized and cropped image data
        resized_io = BytesIO()

        # Save the resized and cropped image to the BytesIO object
        cropped_image.save(resized_io, format='JPEG', quality=image_quality)

        # Create a new InMemoryUploadedFile with the resized and cropped image data
        resized_file = InMemoryUploadedFile(
            resized_io,
            None,
            f"{self.image.name.split('.')[0]}_thumbnail.jpg",  # Name the thumbnail image as per your requirement
            'image/jpeg',
            resized_io.getbuffer().nbytes,
            None
        )

        return resized_file

    def __str__(self):
        return str(self.id)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
