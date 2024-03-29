from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class HomePage(models.Model):
    hero_title = models.CharField(max_length=255, blank=True)
    hero_button_text = models.CharField(max_length=255, blank=True)
    hero_button_link = models.URLField(blank=True)
    hero_image = ProcessedImageField(upload_to='hero_images/',
                                     processors=[ResizeToFill(1920, 1080)],
                                     format='WEBP',
                                     options={'quality': 80})

    def __str__(self):
        return "Homepage Content"