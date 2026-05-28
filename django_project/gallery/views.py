# Create your views here.

from django.shortcuts import render, redirect
from .models import SceneryImage
from .forms import SceneryImageForm


def home(request):

    if request.method == 'POST':
        form = SceneryImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = SceneryImageForm()

    images = SceneryImage.objects.all().order_by('-uploaded_at')

    return render(request, 'gallery/home.html', {
        'form': form,
        'images': images
    })