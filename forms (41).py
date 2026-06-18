import os
from django import forms
from .models import SceneryImage


class SceneryImageForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = SceneryImage
        fields = ['title', 'origin', 'image', 'latitude', 'longitude']
        labels = {
            'title': 'Titel',
            'origin': 'Allgemeiner Ort',
            'image': 'Datei hochladen (.png oder .pdf)',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Titel des Bildes',
                'class': 'form-control',
            }),
            'origin': forms.TextInput(attrs={
                'placeholder': 'z. B. Zürich, Schweiz',
                'class': 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': '.png,.pdf',
                'class': 'form-control-file',
            }),
        }

    def clean_image(self):
        uploaded_file = self.cleaned_data.get('image')

        if uploaded_file:
            extension = os.path.splitext(uploaded_file.name)[1].lower()
            if extension not in ['.png', '.pdf']:
                raise forms.ValidationError('Bitte lade nur .png oder .pdf Dateien hoch.')

        return uploaded_file
