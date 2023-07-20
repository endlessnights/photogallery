from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import SiteSettingsForm
from .models import SiteSettings, Album, Image, MenuItem


def site_settings(request):
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.order_by('order')
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings)

    return render(request, 'front/site_settings.html', {
        'form': form,
        'menu_items': menu_items,
        'settings': settings,
    })


# def reorder_menu_items(request):
#     menu_items = MenuItem.objects.order_by('order')
#     return render(request, 'front/reorder_menu_items.html', {'menu_items': menu_items})


@require_POST
def update_menu_order(request):
    new_order = request.POST.getlist('new_order[]')
    for index, item_id in enumerate(new_order, start=1):
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
            menu_item.order = index
            menu_item.save()
        except MenuItem.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'})


def index_page(request):
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    return render(request, 'front/index.html', {
        'settings': settings,
        'menu_items': menu_items,
    })


def show_albums(request, album_slug):
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    album = Album.objects.get(slug=album_slug)
    images = Image.objects.filter(album=album, status=True).order_by('order')
    context = {
        'album': album,
        'images': images,
        'settings': settings,
        'menu_items': menu_items,
        'album_slug': album_slug,
    }
    return render(request, 'front/album.html', context)


def reorder_albums(request, album_slug):
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    album = Album.objects.get(slug=album_slug)
    albums = Album.objects.all()
    images = Image.objects.filter(album=album).order_by('order')
    context = {
        'album': album,
        'images': images,
        'settings': settings,
        'menu_items': menu_items,
        'albums': albums,
    }
    return render(request, 'front/edit_album.html', context)


def update_image_name(request, photo_id):
    name = request.POST.get('name')
    photo = Image.objects.get(id=photo_id)
    photo.name = name
    photo.save()
    return JsonResponse({'success': True})


def change_album(request, photo_id, album_id):
    photo = Image.objects.get(id=photo_id)
    photo.album_id = album_id
    print('yeeah!')
    photo.save()
    return JsonResponse({'success': True})


def update_image_order(request):
    if request.method == "POST" and request.is_ajax():
        image_order_list = request.POST.get("images")
        image_order_list = json.loads(image_order_list)

        for image_data in image_order_list:
            image_id = image_data["id"]
            new_order = image_data["order"]
            image = Image.objects.get(pk=image_id)
            image.order = new_order
            image.save()

        return JsonResponse({"message": "Image order updated successfully."})
    else:
        return JsonResponse({"message": "Invalid request."}, status=400)


@require_POST
def change_visibility(request, image_id):
    image = Image.objects.get(id=image_id)
    image.status = not image.status
    image.save()
    return JsonResponse({
        'success': True
    })


def upload_images(request):
    albums = Album.objects.all()
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
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
        'settings': settings,
        'menu_items': menu_items,
    })
