from django import forms
from .models import SiteSettings, Image, Album
from django.forms import inlineformset_factory


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            'title',
            'copyright',
            'primary_color',
            'menu_delimiter',
            'title_delimiter',
        )


class ImageForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=Album.objects.all(), empty_label="Select an album", required=False)

    class Meta:
        model = Image
        fields = ['image', 'album']


