from django.shortcuts import render
from gallery.models import SceneryImage
from gallery.forms import SceneryImageForm


def home(request):

    if request.method == "POST":

        form = SceneryImageForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

    form = SceneryImageForm()

    images = SceneryImage.objects.all()

    return render(
        request,
        "blog/home.html",
        {
            "form": form,
            "images": images
        }
    )


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})