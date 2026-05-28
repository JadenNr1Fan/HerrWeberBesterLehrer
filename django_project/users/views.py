from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

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

    return render(request, 'gellery/home.html', {
        'form': form,
        'images': images
    })