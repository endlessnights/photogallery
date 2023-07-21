from django import forms
from .models import SiteSettings, Image, Album
from django.forms import inlineformset_factory


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            'title',
            'title_size',
            'title_delimiter',
            'menu_delimiter',
            'menu_items_size',
            'logo',
            'logo_width',
            'copyright',
            'primary_color',
            'image_long',
            'thumbnail_long',
            'image_quality',
            'thumbnail_quality',
            'preserve_image_size',
        )


class ImageForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=Album.objects.all(), empty_label="Select an album", required=False)

    class Meta:
        model = Image
        fields = ['image', 'album']


