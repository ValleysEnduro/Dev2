from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class HomePage(models.Model):
    page_title = models.CharField(max_length=255, blank=True, verbose_name="Page Title")
    hero_title = models.CharField(max_length=255, blank=True)
    hero_button_text = models.CharField(max_length=255, blank=True)
    hero_button_link = models.URLField(blank=True)
    seo_title = models.CharField(max_length=255, blank=True, help_text="SEO Title")
    seo_meta_description = models.TextField(blank=True, help_text="SEO Meta Description")
    seo_keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")
    social_title = models.CharField(max_length=255, blank=True, help_text="Social Sharing Title")
    social_description = models.TextField(blank=True, help_text="Social Sharing Description")
    social_image = models.ImageField(upload_to='social_images/', blank=True, help_text="Social Sharing Image")
    social_image_alt = models.CharField(max_length=255, blank=True, help_text="Social Image Alt Text")
    hero_image = ProcessedImageField(
        upload_to='hero_images/',
        processors=[ResizeToFill(1920, 1080)],
        format='WEBP',
        options={'quality': 80}
    
    )

    def __str__(self):
        return self.page_title or "Homepage"

class RefundPolicy(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(null=True)
    last_updated = models.DateTimeField(auto_now=True)
    cutoff_days = models.IntegerField(help_text="Number of days before the event when refunds are no longer available.")
    refund_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage of the entry fee that will be refunded if cancelled before the cutoff.")

    def __str__(self):
        return f"Refund Policy updated on {self.last_updated.strftime('%Y-%m-%d')}"
    
class PrivacyPolicy(models.Model):
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Privacy Policy updated on {self.last_updated.strftime('%Y-%m-%d')}"
