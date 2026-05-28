from django.db import models

# Create your models here.

from django.db import models


class SceneryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='scenery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title