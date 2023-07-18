from django.shortcuts import render, redirect

from .forms import SiteSettingsForm
from .models import SiteSettings, Album, Image


def site_settings(request):
    settings = SiteSettings.objects.first()  # Assuming you only have one settings object

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('site_settings')  # Redirect back to the settings page after saving
    else:
        form = SiteSettingsForm(instance=settings)

    return render(request, 'front/site_settings.html', {'form': form})


def upload_images(request):
    albums = Album.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('image')
        if data['album'] != 'none':
            album = Album.objects.get(name=data['album'])
        else:
            album = None

        for image in images:
            image_obj = Image.objects.create(
                album=album,
                image=image,
            )
            target_size = (800, 800)
            thumbnail = image_obj.resize_and_crop(target_size)
            image_obj.thumbnail = thumbnail
            image_obj.save()
        return redirect(upload_images)

    return render(request, 'front/upload.html', {
        'albums': albums,
    })


# thumbnail = image.create_thumbnail()
# image.thumbnail = thumbnail