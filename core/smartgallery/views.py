from django.shortcuts import render
from django.views import View


class ShowAlbum(View):
    def get(self, request, getpfcategory):
        showposts = subcategory.objects.annotate(posts_count=Count('subcategory')).filter(
            category__slug=getpfcategory)
        return render(request, 'site/categories.html', {
            'showposts': showposts,
        }
                      )