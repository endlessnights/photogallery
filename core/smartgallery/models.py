import datetime
import os
from io import BytesIO
from PIL import ImageOps
from PIL.ExifTags import TAGS
from PIL import Image as PILImage, ExifTags
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class SiteSettings(models.Model):
    title = models.CharField(verbose_name=_('Website title'), max_length=100, blank=True, default='Smart Photo Gallery')
    logo = models.FileField(verbose_name=_('Site logo'), upload_to='logo/', blank=True)
    logo_width = models.PositiveIntegerField(verbose_name=_('Logo width, px'), blank=True, default=240)
    topbar_bgcolor = models.CharField(verbose_name=_('Top bar Background Color'), max_length=8, default="#B7C3F3", blank=True)
    topbar_fcolor = models.CharField(verbose_name=_('Top bar Font Color'), max_length=8, default="black", blank=True)
    copyright = models.CharField(
        verbose_name=_('Copyright text'),
        max_length=1000,
        blank=True,
        default=f'Smart Photo Gallery - {datetime.datetime.now().year}'
    )
    menu_delimiter = models.CharField(verbose_name=_('Menu delimiter'), max_length=5, blank=True, default=' | ')
    title_delimiter = models.CharField(verbose_name=_('Title delimiter'), max_length=5, blank=True, default=' · ')
    title_size = models.PositiveIntegerField(verbose_name=_('Title size, h1-6'), blank=True, default=2)
    menu_items_size = models.PositiveIntegerField(verbose_name=_('Menu item size, pt'), blank=True, default=18)
    image_long = models.PositiveIntegerField(verbose_name=_('Big image long side, px'), blank=False, default=1600)
    thumbnail_long = models.PositiveIntegerField(verbose_name=_('Preview long side, px'), blank=False, default=800)
    image_quality = models.PositiveIntegerField(verbose_name=_('Big image quality, %'), blank=False, default=90)
    thumbnail_quality = models.PositiveIntegerField(verbose_name=_('Preview image quality, %'), blank=False, default=80)
    preserve_image_size = models.BooleanField(verbose_name=_('Preserve big image size and quality'), default=False)
    show_social_links = models.BooleanField(verbose_name=_('Show social links'), default=False)
    show_about_page = models.BooleanField(verbose_name=_('Show About Me'), default=False)
    show_timeline_page = models.BooleanField(verbose_name=_('Show Timeline'), default=False)
    favicon = models.FileField(verbose_name=_('Favicon'), upload_to='favicon/', max_length=250, blank=True)
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Russian'),
    ]
    default_language = models.CharField(
        verbose_name=_('Default Language'),
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en',  # Set the default language
    )
    gle_analytics = models.TextField(verbose_name=_('Google analytics code'), max_length=1000, blank=True)
    index_content = models.TextField(verbose_name=_('Index page content'), max_length=20000, blank=True, default='')
    about_content = models.TextField(verbose_name=_('About me page content'), max_length=20000, blank=True, default='')

    def render_index_content(self, context=None):
        from django.template import Template, Context

        if context is None:
            context = {}

        template = Template(self.index_content)
        context = Context(context)
        return template.render(context)

    def render_about_content(self, context=None):
        from django.template import Template, Context

        if context is None:
            context = {}

        template = Template(self.about_content)
        context = Context(context)
        return template.render(context)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Site settings')
        verbose_name_plural = _('Site settings')


class SocialLinks(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=80, blank=False)
    link = models.CharField(verbose_name=_('Link'), max_length=200, blank=True)
    icon = models.CharField(verbose_name=_('Icon'), max_length=100, blank=True)
    order = models.PositiveIntegerField(verbose_name=_('Order'), default=0)

    def __str__(self):
        return str(self.name)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')


class Album(models.Model):
    slug = models.CharField(verbose_name=_('SLUG'), max_length=128, blank=False, null=False)
    name = models.CharField(verbose_name=_('Album name'), max_length=128, blank=False, null=False)
    meta_tags = models.CharField(verbose_name=_('Meta keywords'), max_length=1000, blank=True)
    meta_desc = models.CharField(verbose_name=_('Meta description'), max_length=1000, blank=True)
    desc = models.TextField(
        verbose_name=_('About album'),
        max_length=2000,
        default=('Album description can be changed in Album settings'),
        blank=True,
        null=True
    )
    desc_visible = models.BooleanField(verbose_name=_('Description visibility'), default=True)
    cols_count_s = models.PositiveIntegerField(verbose_name=_('Columns count on mobile devices'), default=2)
    cols_count_m = models.PositiveIntegerField(verbose_name=_('Columns count'), default=3)
    cols_gap_size = [
        ('cl', "collapse"),
        ('sm', "small"),
        ('md', "medium"),
        ('lg', "large"),
    ]
    cols_gap = models.CharField(
        verbose_name=_('Columns gap'),
        max_length=2,
        choices=cols_gap_size,
        default='sm',
    )
    grid_types = [
        ('grid', "grid"),
        ('masonry', "masonry (beta)"),
    ]
    grid_type = models.CharField(
        verbose_name=_('Grid type'),
        max_length=10,
        choices=grid_types,
        default='grid',
    )
    masonry_text_overlay = models.BooleanField(verbose_name=_('Masonry text overlay'), default=True)
    image_border_radius = models.PositiveIntegerField(verbose_name=_('Images border radius, px'), default=0, blank=False)
    order = models.PositiveIntegerField(verbose_name=_('Order'), blank=True, null=True, default=0)
    status = models.BooleanField(verbose_name=_('Visibility'), default=True)
    transitions = [
        ('fade', "fade"),
        ('slide', "slide"),
        ('scale', "scale"),
    ]
    transition_anim = models.CharField(
        verbose_name=_('Image transition'),
        max_length=6,
        choices=transitions,
        default='slide',
    )
    cover = models.ImageField(upload_to=('album_covers'), blank=True, null=True)
    cover_visible = models.BooleanField(verbose_name=_('Cover visibility'), default=False)

    def resize_and_crop_cover(self, cover_long, cover_quality):
        # Open the original image using PIL
        pil_image = PILImage.open(self.cover.path)

        # Get the size of the original image
        width, height = pil_image.size

        # Calculate the aspect ratio of the original image
        aspect_ratio = width / height

        # Calculate the new size based on the provided long side while preserving the aspect ratio
        if width > height:
            new_width = cover_long
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = cover_long
            new_width = int(new_height * aspect_ratio)

        # Resize the image using the new size while preserving the aspect ratio
        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

        pil_image = pil_image.convert('RGB')

        # Create a BytesIO object to store the resized image data
        resized_io = BytesIO()

        # Save the resized image to the BytesIO object
        pil_image.save(resized_io, format='JPEG', quality=cover_quality, subsampling=0)

        # Create a new InMemoryUploadedFile with the resized image data
        resized_file = InMemoryUploadedFile(
            resized_io,
            None,
            f"{self.cover.name.split('.')[0]}_resized.jpg",
            'image/jpeg',
            resized_io.getbuffer().nbytes,
            None
        )

        # Update the cover field with the resized image
        self.cover = resized_file
        self.save()

        return self.cover

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')


class MenuItem(models.Model):
    album = models.OneToOneField('Album', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=120)
    order = models.PositiveIntegerField(verbose_name=_('Order'), default=0)
    privilege = models.BooleanField(verbose_name=_('Menu title privilege'), default=False)
    status = models.BooleanField(verbose_name=_('Visibility'), default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


def image_path(instance, filename):
    # instance.album.slug contains the name of the Album
    # filename contains the original filename of the uploaded image
    return os.path.join('image', instance.album.slug, filename)


def thumbnail_path(instance, filename):
    # instance.album.slug contains the name of the Album
    # filename contains the original filename of the uploaded image
    return os.path.join('thumbnails', instance.album.slug, filename)


class Image(models.Model):
    name = models.CharField(verbose_name=_('Image name'), max_length=250, blank=True, null=True)
    src_image = models.ImageField(upload_to=image_path, blank=True)
    image = models.ImageField(upload_to=image_path)

    thumbnail = models.ImageField(upload_to=thumbnail_path, blank=True, null=True)
    ytvideo = models.CharField(verbose_name=_('Youtube Video link'), max_length=200, blank=True, null=True)
    album = models.ForeignKey(Album,
                              on_delete=models.PROTECT,
                              verbose_name=_('Choose Album'))
    order = models.PositiveIntegerField(verbose_name=_('Order'), blank=True, default=0)
    status = models.BooleanField(verbose_name=_('Visibility'), default=True)

    camera_manufacturer = models.CharField(max_length=100, blank=True, null=True)
    camera_model = models.CharField(max_length=100, blank=True, null=True)
    focal_length = models.CharField(verbose_name=_('Focal Length'), max_length=10, blank=True, null=True)
    exposure_time = models.CharField(max_length=50, blank=True, null=True)
    f_number = models.CharField(max_length=50, blank=True, null=True)
    iso_speed = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(verbose_name=_('Latitude'), blank=True, null=True)
    longitude = models.FloatField(verbose_name=_('Longitude'), blank=True, null=True)
    date_taken = models.DateTimeField(blank=True, null=True)

    def resize_and_crop(self, long_side, image_quality):
        # Open the original image using PIL

        self.src_image = self.image

        pil_image = PILImage.open(self.image.path)

        if pil_image.format == "WEBP":
            pil_image = pil_image.convert("RGB")

        # Get the size of the original image
        width, height = pil_image.size

        # Calculate the aspect ratio of the original image
        aspect_ratio = width / height

        # Calculate the new size based on the provided long side while preserving the aspect ratio
        if width > height:
            new_width = long_side
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = long_side
            new_width = int(new_height * aspect_ratio)

        # Resize the image using the new size while preserving the aspect ratio
        pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

        pil_image = ImageOps.exif_transpose(pil_image)

        pil_image = pil_image.convert('RGB')

        # Create a BytesIO object to store the resized image data
        resized_io = BytesIO()

        # Save the resized image to the BytesIO object
        try:
            pil_image.save(resized_io, format='JPEG', quality=image_quality, subsampling=0)
        except FileNotFoundError:
            # Handle the case where the temporary file can't be deleted
            pass

        # Create a new InMemoryUploadedFile with the resized image data
        resized_file = InMemoryUploadedFile(
            resized_io,
            None,
            f"{self.image.name.split('.')[0]}_resized.jpg",
            'image/jpeg',
            resized_io.getbuffer().nbytes,
            None
        )

        return resized_file

    def save(self, *args, **kwargs):
        # Read EXIF data from the image and populate the fields
        if self.image:
            img = PILImage.open(self.image)
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'Make':
                        self.camera_manufacturer = value
                    elif tag_name == 'Model':
                        self.camera_model = f"'{value}'"
                    elif tag_name == 'ExposureTime':
                        try:
                            exposure_time = float(value)
                            exposure_time = 1 / exposure_time
                            self.exposure_time = f"1/{str(round(exposure_time, 5)).replace('.0', '')}s"
                        except:
                            print('Could not take exposure time data from exif')
                    elif tag_name == 'FNumber':
                        self.f_number = f"f/{str(value)}"
                    elif tag_name == 'FocalLength':
                        # Convert IFDRational to float for focal length
                        self.focal_length = f"{str(value)}mm"
                    elif tag_name == 'ISOSpeedRatings':
                        self.iso_speed = f"ISO {str(value)}"
                    elif tag_name == 'GPSInfo':
                        gps_info = {ExifTags.GPSTAGS.get(t, t): v for t, v in value.items()}
                        latitude_ref = gps_info.get('GPSLatitudeRef')
                        latitude = gps_info.get('GPSLatitude')
                        longitude_ref = gps_info.get('GPSLongitudeRef')
                        longitude = gps_info.get('GPSLongitude')

                        if latitude and latitude_ref and longitude and longitude_ref:
                            lat_deg, lat_min, lat_sec = latitude
                            lon_deg, lon_min, lon_sec = longitude
                            latitude = (lat_deg + lat_min / 60 + lat_sec / 3600) * (-1 if latitude_ref == 'S' else 1)
                            longitude = (lon_deg + lon_min / 60 + lon_sec / 3600) * (-1 if longitude_ref == 'W' else 1)
                            self.latitude = latitude
                            self.longitude = longitude

                    elif tag_name == 'DateTimeOriginal':
                        naive_datetime = timezone.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        self.date_taken = timezone.make_aware(naive_datetime)

                orientation = exif_data.get(0x0112)
                if orientation is not None:
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(-90, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
