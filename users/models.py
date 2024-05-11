# users/models.py
import os
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_upload_to(instance, filename):
    username_slug = slugify(instance.username)
    extension = os.path.splitext(filename)[1]
    new_filename = f"{username_slug}{extension}"
    return os.path.join('avatars', new_filename)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_upload_to, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

class Purchase(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)
