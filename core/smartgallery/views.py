import json
import os
from django.conf import settings as global_settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import activate
from django.views.decorators.http import require_POST
from .forms import SiteSettingsForm, CreateAlbumView, EditAlbumForm, SocialForm, UserSettingsForm, \
    PasswordChangeCustomForm, EditHTMLPages
from .models import SiteSettings, Album, Image, MenuItem, SocialLinks
from django.template.defaulttags import register


@register.filter
def replace_commas_with_periods(value):
    return value.replace(',', '.')


def site_settings(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.order_by('order')
    social = SocialLinks.objects.all().order_by('order')
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('site_settings')
    else:
        form = SiteSettingsForm(instance=settings)
        print(form.errors)

    return render(request, 'front/settings/site_settings.html', {
        'form': form,
        "menu_items": menu_items,
        'settings': settings,
        'social': social,
        'settings_instance': settings_instance,
    })


@login_required
def template_settings(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.order_by('order')
    social = SocialLinks.objects.all().order_by('order')
    if request.method == 'POST':
        form = EditHTMLPages(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('template_settings')
    else:
        form = EditHTMLPages(instance=settings)
        print(form.errors)

    return render(request, 'front/settings/template_settings.html', {
        'form': form,
        "menu_items": menu_items,
        'settings': settings,
        'social': social,
        'settings_instance': settings_instance,
    })



@login_required
def delete_current_logo(request):
    settings = SiteSettings.objects.first()
    os.remove(settings.logo.path)
    settings.logo.delete()
    settings.save()
    return redirect('site_settings')


def menu_settings(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.order_by('order')
    social = SocialLinks.objects.all().order_by('order')
    return render(request, 'front/settings/menu_settings.html', {
        "menu_items": menu_items,
        "settings": settings,
        "social": social,
    })


@login_required
def user_settings(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.order_by('order')
    social = SocialLinks.objects.all().order_by('order')
    user = request.user

    if request.method == 'POST':
        user_form = UserSettingsForm(request.POST, instance=user)
        password_form = PasswordChangeCustomForm(user, request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('user_settings')  # Redirect to a success page

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to update session
            return redirect('user_settings')  # Redirect to a success page
    else:
        user_form = UserSettingsForm(instance=user, initial={'email': user.email})
        password_form = PasswordChangeCustomForm(user)

    return render(request, 'front/settings/user_settings.html', {
        'user_form': user_form,
        'password_form': password_form,
        "menu_items": menu_items,
        "settings": settings,
        "social": social,
    })


@login_required
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


@login_required
@require_POST
def update_social_order(request):
    new_order = request.POST.getlist('new_order[]')
    for index, item_id in enumerate(new_order, start=1):
        try:
            social_item = SocialLinks.objects.get(id=int(item_id))
            social_item.order = index
            social_item.save()
        except SocialLinks.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'})


@login_required
@require_POST
def update_menu_item_name(request):
    item_id = request.POST.get("item_id")
    new_name = request.POST.get("new_name")
    new_privilege = request.POST.get("privilege")
    new_status = request.POST.get("status")
    if new_privilege == "true":
        new_privilege = True
    else:
        new_privilege = False
    if new_status == "true":
        new_status = True
    else:
        new_status = False
    try:
        menu_item = MenuItem.objects.get(id=item_id)
        menu_item.name = new_name
        menu_item.save()
        menu_item.privilege = new_privilege
        menu_item.save()
        menu_item.status = new_status
        menu_item.save()
        return JsonResponse({"status": "success", "message": "Menu item name updated successfully."})
    except MenuItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Menu item not found."}, status=404)


@login_required
@require_POST
def update_social_item_name(request):
    item_id = request.POST.get("item_id")
    new_name = request.POST.get("new_name")
    new_link = request.POST.get("new_link")
    new_icon = request.POST.get("new_icon")
    try:
        social_item = SocialLinks.objects.get(id=item_id)
        social_item.name = new_name
        social_item.save()
        social_item.link = new_link
        social_item.save()
        social_item.icon = new_icon
        social_item.save()
        return JsonResponse({"status": "success", "message": "Menu item name updated successfully."})
    except MenuItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Menu item not found."}, status=404)


@login_required
def delete_social_item_name(request, id):
    social_item = SocialLinks.objects.get(id=id)
    social_item.delete()
    return redirect('social_settings')


def index_page(request):
    social = SocialLinks.objects.all().order_by('order')
    settings = SiteSettings.objects.first()
    albums = Album.objects.all()
    menu_items = MenuItem.objects.all()
    images = Image.objects.all()

    rendered_content = settings.render_index_content({
        'menu_items': menu_items,
        'settings': settings,
        'albums': albums,
        'social': social,
        'images': images,
    })

    return render(request, 'front/index_safe.html', {
        'settings': settings,
        'menu_items': menu_items,
        'rendered_content': rendered_content,
        'social': social,
        'images': images,
    })


@login_required
def social_settings(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    social = SocialLinks.objects.all().order_by('order')
    if request.method == "POST":
        form = SocialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('social_settings')
    else:
        form = SocialForm()

    return render(request, 'front/settings/social_settings.html', {
        'form': form,
        'menu_items': menu_items,
        'settings': settings,
        'social': social,
    })


def timeline(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    menu_items = MenuItem.objects.all()
    social = SocialLinks.objects.all().order_by('order')
    images = Image.objects.order_by('-date_taken')
    timeline_dict = {}

    for image in images:
        if image.date_taken:
            year = image.date_taken.year
            if year not in timeline_dict:
                timeline_dict[year] = []
            timeline_dict[year].append(image)

    # Add images with no date to the end of the timeline
    no_date_images = Image.objects.filter(date_taken__isnull=True)
    if no_date_images.exists():
        timeline_dict['No date'] = list(no_date_images)

    context = {
        'timeline': timeline_dict,
        'menu_items': menu_items,
        'settings': settings,
        'social': social,
    }
    return render(request, 'front/timeline.html', context)


def show_albums(request, album_slug):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    social = SocialLinks.objects.all()
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
        'social': social,
        'settings_instance': settings_instance,
    }
    return render(request, 'front/album.html', context)


@login_required
def create_album(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    social = SocialLinks.objects.all().order_by('order')
    menu_items = MenuItem.objects.all()
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
            if album.cover:
                album.resize_and_crop_cover(cover_long, cover_quality)  # Resize and crop the cover image
            return redirect('show_albums', album.slug)

    else:
        form = CreateAlbumView()

    return render(request, 'front/create_album.html', {
        'form': form,
        'settings': settings,
        'menu_items': menu_items,
        'social': social,
    })


@login_required
def edit_album(request, album_id):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    album = Album.objects.get(id=album_id)
    settings = SiteSettings.objects.first()
    social = SocialLinks.objects.all().order_by('order')
    menu_items = MenuItem.objects.all()
    albums = Album.objects.all()
    images = Image.objects.filter(album=album).order_by('order')
    name = request.POST.get('name')
    slug = request.POST.get('slug')
    preferred_language = request.COOKIES.get(global_settings.LANGUAGE_COOKIE_NAME, None)
    if preferred_language and preferred_language in [code for code, _ in global_settings.LANGUAGES]:
        # Activate the preferred language
        activate(preferred_language)
    if Album.objects.filter(name=name).exclude(id=album_id).exists() or Album.objects.filter(slug=slug).exclude(
            id=album_id).exists():
        error_msg = "Album with the same name or slug already exists."
        return render(request, 'front/edit_album.html',
                      {
                          'album': album,
                          'images': images,
                          'settings': settings,
                          'menu_items': menu_items,
                          'albums': albums,
                          'error_msg': error_msg,
                          'settings_instance': settings_instance,
                      })
    if request.method == "POST":
        cols_gap_key = album.cols_gap
        form = EditAlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    context = {
        'album': album,
        'images': images,
        'settings': settings,
        'menu_items': menu_items,
        'albums': albums,
        'social': social,
        'settings_instance': settings_instance,
    }
    return render(request, 'front/edit_album.html', context)


@login_required
def delete_image(request, image_id):
    image_obj = Image.objects.get(id=image_id)
    image_path = os.path.join(global_settings.MEDIA_ROOT, str(image_obj.image))
    thumbnail_path = os.path.join(global_settings.MEDIA_ROOT, str(image_obj.thumbnail))
    src_image_path = os.path.join(global_settings.MEDIA_ROOT, str(image_obj.src_image))
    if os.path.exists(image_path):
        os.remove(image_path)
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    if os.path.exists(src_image_path):
        os.remove(src_image_path)
    image_obj.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        # Delete all images associated with the album
        images_to_delete = Image.objects.filter(album=album)
        for image in images_to_delete:
            image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.image))
            thumbnail_path = os.path.join(global_settings.MEDIA_ROOT, str(image.thumbnail))
            src_image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.src_image))

            # Delete the files from disk
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            if os.path.exists(src_image_path):
                os.remove(src_image_path)
        images_to_delete.delete()
        print('all images deleted')
        album.delete()
        print('album deleted')
        response_data = {'status': 'success', 'redirect_url': 'settings'}
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def delete_all_album_images(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        # Delete all images associated with the album
        images_to_delete = Image.objects.filter(album=album)
        for image in images_to_delete:
            image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.image))
            thumbnail_path = os.path.join(global_settings.MEDIA_ROOT, str(image.thumbnail))
            src_image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.src_image))

            # Delete the files from disk
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            if os.path.exists(src_image_path):
                os.remove(src_image_path)

            # Delete all images associated with the album from the database
        images_to_delete.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def delete_all_album_hidden_images(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if request.method == 'POST':
        # Delete all images associated with the album
        images_to_delete = Image.objects.filter(album=album, status=False)
        for image in images_to_delete:
            image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.image))
            thumbnail_path = os.path.join(global_settings.MEDIA_ROOT, str(image.thumbnail))
            src_image_path = os.path.join(global_settings.MEDIA_ROOT, str(image.src_image))

            # Delete the files from disk
            if os.path.exists(image_path):
                os.remove(image_path)
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            if os.path.exists(src_image_path):
                os.remove(src_image_path)

            # Delete all images associated with the album from the database
        images_to_delete.delete()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def update_image_name(request, photo_id):
    name = request.POST.get('name')
    photo = Image.objects.get(id=photo_id)
    photo.name = name
    photo.save()
    return JsonResponse({'success': True})


@login_required
def update_image_exif(request, photo_id):
    fields = ['camera_manufacturer', 'camera_model', 'focal_length',
              'exposure_time', 'f_number', 'iso_speed', 'latitude', 'longitude', 'date_taken']

    data = {field: request.POST.get(field) for field in fields}
    photo = Image.objects.get(id=photo_id)

    for field, value in data.items():
        if field in ['latitude', 'longitude']:
            value = value.replace(',', '.')
        setattr(photo, field, value)
        print(field, value)
    photo.save()

    return JsonResponse({'success': True})


@login_required
def change_album(request, photo_id, album_id):
    photo = Image.objects.get(id=photo_id)
    photo.album_id = album_id
    photo.save()
    return JsonResponse({'success': True})


@login_required
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


@login_required
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


@login_required
def upload_images(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    albums = Album.objects.all()
    settings = SiteSettings.objects.first()
    social = SocialLinks.objects.all().order_by('order')
    preserve_image_size = False
    if settings.preserve_image_size:
        print('preserve_image_size in view')
        preserve_image_size = True
        image_quality = 100
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('image')
        ytvideo = request.POST.get('ytvideo')
        if data['album'] != 'none':
            album = Album.objects.get(name=data['album'])
        else:
            album = None

        for image_item in images:
            image_obj = Image.objects.create(
                album=album,
                image=image_item,
                ytvideo=ytvideo,
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
        'social': social,
    })


def about(request):
    settings_instance = SiteSettings.objects.first()
    if settings_instance:
        activate(settings_instance.default_language)
        global_settings.LANGUAGE_CODE = settings_instance.default_language
    settings = SiteSettings.objects.first()
    social = SocialLinks.objects.all().order_by('order')
    menu_items = MenuItem.objects.all()
    albums = Album.objects.all()
    images = Image.objects.all()

    rendered_content = settings.render_about_content({
        'menu_items': menu_items,
        'settings': settings,
        'albums': albums,
        'social': social,
        'images': images,
    })

    return render(request, 'front/about.html', {
        'settings': settings,
        'menu_items': menu_items,
        'social': social,
        'albums': albums,
        'rendered_content': rendered_content,
    })
