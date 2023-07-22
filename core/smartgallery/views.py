from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .forms import SiteSettingsForm, CreateAlbumView, EditAlbumForm
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


@require_POST
def update_menu_item_name(request):
    item_id = request.POST.get("item_id")
    new_name = request.POST.get("new_name")
    try:
        menu_item = MenuItem.objects.get(id=item_id)
        menu_item.name = new_name
        menu_item.save()
        return JsonResponse({"status": "success", "message": "Menu item name updated successfully."})
    except MenuItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Menu item not found."}, status=404)


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


def create_album(request):
    cover_long = 2000
    cover_quality = 90
    if request.method == 'POST':
        form = CreateAlbumView(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            slug = form.cleaned_data['slug']

            # Check if the album with the same name or slug already exists
            if Album.objects.filter(name=name).exists() or Album.objects.filter(slug=slug).exists():
                error_msg = "Album with the same name or slug already exists."
                return render(request, 'front/create_album.html', {'form': form, 'error_msg': error_msg})

            album = form.save()
            album.resize_and_crop_cover(cover_long, cover_quality)  # Resize and crop the cover image
            return redirect('show_albums', album.slug)

    else:
        form = CreateAlbumView()

    return render(request, 'front/create_album.html', {'form': form})


def reorder_albums(request, album_id):
    album = Album.objects.get(id=album_id)
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    albums = Album.objects.all()
    images = Image.objects.filter(album=album).order_by('order')
    if request.method == "POST":
        cols_gap_key = album.cols_gap
        print(cols_gap_key)
        form = EditAlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            print('ss')
            form.save()
            return redirect(request.META['HTTP_REFERER'])
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


def resize_thumbnails(settings, image_obj):
    if settings.thumbnail_long and settings.thumbnail_quality:
        thumbnail_long_side = settings.thumbnail_long
        thumbnail_quality = settings.thumbnail_quality
    else:
        thumbnail_long_side = 800
        thumbnail_quality = 80
    resized_thumbnail = image_obj.resize_and_crop(thumbnail_long_side, thumbnail_quality)
    image_obj.thumbnail = resized_thumbnail

    return image_obj


def upload_images(request):
    albums = Album.objects.all()
    settings = SiteSettings.objects.first()
    preserve_image_size = False
    if settings.preserve_image_size:
        print('preserve_image_size in view')
        preserve_image_size = True
        image_quality = 100
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
            #   If SiteSetting.preserve_image_size == False, crop and change quality of images and thumbnails
            if not preserve_image_size:
                if settings.image_long and settings.image_quality:
                    image_long_side = settings.image_long
                    image_quality = settings.image_quality
                else:
                    image_long_side = 1600
                    image_quality = 90
                resize_thumbnails(settings, image_obj)
                resized_image = image_obj.resize_and_crop(image_long_side, image_quality)
                image_obj.image = resized_image
                image_obj.save()
            #   If SiteSetting.preserve_image_size == True, crop and change quality only of thumbnails
            else:
                resize_thumbnails(settings, image_obj)
                image_obj.save()
        return redirect(upload_images)

    return render(request, 'front/upload.html', {
        'albums': albums,
        'settings': settings,
        'menu_items': menu_items,
    })
