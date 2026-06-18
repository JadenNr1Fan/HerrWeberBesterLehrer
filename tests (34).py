import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from gallery.forms import SceneryImageForm
from gallery.models import SceneryImage


def _image_payload(img):
    return {
        'id': img.id,
        'title': img.title,
        'origin': img.origin,
        'url': img.image.url,
        'latitude': img.latitude,
        'longitude': img.longitude,
        'likes': img.likes,
        'dislikes': img.dislikes,
        'score': img.score,
        'is_pdf': img.is_pdf,
    }


def home(request):
    if request.method == 'POST':
        form = SceneryImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = SceneryImageForm()

    images = SceneryImage.objects.all().order_by('-uploaded_at')
    image_data = [_image_payload(img) for img in images]
    top_images = sorted(image_data, key=lambda item: (item['likes'], item['score']), reverse=True)[:3]

    return render(request, 'blog/home.html', {
        'form': form,
        'images': images,
        'image_data_json': json.dumps(image_data),
        'top_images_json': json.dumps(top_images),
    })


@require_POST
def vote_image(request, image_id):
    image = get_object_or_404(SceneryImage, id=image_id)
    vote_type = request.POST.get('vote')

    if vote_type == 'like':
        image.likes += 1
    elif vote_type == 'dislike':
        image.dislikes += 1
    else:
        return JsonResponse({'error': 'Ungültige Bewertung.'}, status=400)

    image.save(update_fields=['likes', 'dislikes'])

    return JsonResponse({
        'id': image.id,
        'likes': image.likes,
        'dislikes': image.dislikes,
        'score': image.score,
    })


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
