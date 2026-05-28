from django import forms
from .models import SceneryImage


class SceneryImageForm(forms.ModelForm):
    class Meta:
        model = SceneryImage
        fields = ['title', 'image']