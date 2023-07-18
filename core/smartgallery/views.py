from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import SiteSettingsForm
from .models import SiteSettings, Album, Image


def site_settings(request):
    settings = SiteSettings.objects.first()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings)

    return render(request, 'front/site_settings.html', {'form': form})


def show_albums(request, album_slug):
    settings = SiteSettings.objects.first()
    album = Album.objects.get(slug=album_slug)
    images = Image.objects.filter(album=album).order_by('order')
    context = {
        'album': album,
        'images': images,
        'settings': settings,
    }
    return render(request, 'front/album.html', context)


def reorder_albums(request, album_slug):
    settings = SiteSettings.objects.first()
    album = Album.objects.get(slug=album_slug)
    images = Image.objects.filter(album=album).order_by('order')
    context = {
        'album': album,
        'images': images,
        'settings': settings,
    }
    return render(request, 'front/reorder_album.html', context)


def update_image_order(request):
    if request.method == "POST" and request.is_ajax():
        image_order_data = request.POST.get("images")
        image_order_data = json.loads(image_order_data)

        for image_data in image_order_data:
            image_id = image_data["id"]
            new_order = image_data["order"]
            image = Image.objects.get(pk=image_id)
            image.order = new_order
            image.save()

        return JsonResponse({"message": "Image order updated successfully."})
    else:
        return JsonResponse({"message": "Invalid request."}, status=400)


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

            # canvas_size = (800, 800)
            # thumbnail = image_obj.resize_and_crop(canvas_size)
            # image_obj.thumbnail = thumbnail
            # image_obj.save()

            long_side = 800
            resized_image = image_obj.resize_and_crop(long_side)
            image_obj.thumbnail = resized_image
            image_obj.save()
        return redirect(upload_images)

    return render(request, 'front/upload.html', {
        'albums': albums,
    })

