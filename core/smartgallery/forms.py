from django import forms
from .models import SiteSettings, Image, Album, AboutPage, SocialLinks
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
            'topbar_bgcolor',
            'topbar_fcolor',
            'image_long',
            'thumbnail_long',
            'image_quality',
            'thumbnail_quality',
            'preserve_image_size',
            'show_social_links',
            'show_about_page',
            'favicon',
        )


class CreateAlbumView(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'name',
            'desc',
            'slug',
            'cover',
            'status',
        ]


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialLinks
        fields = [
            'name',
            'link',
            'icon',
        ]


class EditAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = [
            'name',
            'slug',
            'desc',
            'desc_visible',
            'cover_visible',
            'cols_count_s',
            'cols_count_m',
            'cols_gap',
            'image_border_radius',
            'status',
            'transition_anim',
            'cover',
            'meta_tags',
            'meta_desc',
        ]


class EditAboutForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = [
            'name',
            'content',
            'meta_tags',
            'meta_desc',
        ]


class ImageForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=Album.objects.all(), empty_label="Select an album", required=False)

    class Meta:
        model = Image
        fields = [
            'image',
            'album',
            'ytvideo',
        ]
