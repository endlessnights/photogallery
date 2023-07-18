from django.db import models
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Album(models.Model):
    slug = models.CharField(verbose_name='SLUG', max_length=128, blank=False, null=False)
    name = models.CharField(verbose_name='Album name', max_length=128, blank=False, null=False)
    desc = models.TextField(verbose_name='About album', max_length=2000, blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name='Order', blank=True)
    status = models.BooleanField(verbose_name='Visibility', default=True)
    cover = ProcessedImageField(upload_to='album_covers',
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality': 90},
                                verbose_name='Album Cover image',
                                blank=True,)

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class Image(models.Model):
    name = models.CharField(verbose_name='Image name', max_length=250, blank=False, null=False)
    image = models.ImageField(upload_to=f'album_covers/{Album.slug}/')
    thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(800, 800)],
                                      format='JPEG',
                                      options={'quality': 80})
    album = models.ForeignKey(Album,
                              on_delete=models.PROTECT,
                              verbose_name='Choose Album')
    order = models.PositiveIntegerField(verbose_name='Order', blank=True)
    status = models.BooleanField(verbose_name='Visibility', default=True)

    def __str__(self):
        return self.name

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
