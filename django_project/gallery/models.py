from django.db import models


class SceneryImage(models.Model):
    title = models.CharField(max_length=100)
    origin = models.CharField(
        max_length=120,
        default="Switzerland",
        help_text="Zum Beispiel: Switzerland, Zürich, Paris, Japan"
    )
    image = models.ImageField(upload_to='scenery_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.origin}"