from django.db import models


class SceneryImage(models.Model):
    title = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='scenery_images/'
    )

    latitude = models.FloatField(default=46.8182)
    longitude = models.FloatField(default=8.2275)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

latitude = models.FloatField(...)
longitude = models.FloatField(...)