from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    seo_title = models.CharField(max_length=200, blank=True)
    seo_meta_description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='posts_media/', blank=True, null=True)
    alt_media_description = models.CharField(max_length=200, blank=True)
    document = models.FileField(upload_to='posts_documents/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title