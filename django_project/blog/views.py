import json
from django.shortcuts import render, redirect
from gallery.forms import SceneryImageForm
from gallery.models import SceneryImage


def home(request):
    if request.method == 'POST':
        form = SceneryImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = SceneryImageForm()

    images = SceneryImage.objects.all().order_by('-uploaded_at')

    image_data = []

    for img in images:
        image_data.append({
            'title': img.title,
            'origin': img.origin,
            'url': img.image.url,
        })

    return render(request, 'blog/home.html', {
        'form': form,
        'images': images,
        'image_data_json': json.dumps(image_data),
    })


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})