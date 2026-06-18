import os
from django import forms
from .models import SceneryImage


class SceneryImageForm(forms.ModelForm):

    class Meta:
        model = SceneryImage
        fields = ['title', 'origin', 'image']
        labels = {
            'title': 'Titel',
            'origin': 'Ort / Land, woher das Bild stammt',
            'image': 'Bild hochladen (.png, .jpg, .jpeg)',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            extension = os.path.splitext(image.name)[1].lower()

            if extension not in ['.png', '.jpg', '.jpeg']:
                raise forms.ValidationError('Bitte lade nur .png, .jpg oder .jpeg Bilder hoch.')

        return image