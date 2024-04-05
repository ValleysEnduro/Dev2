from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')  # Example choices could be 'pending', 'completed', 'failed'
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # GenericForeignKey setup
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Additional fields as necessary (e.g., Stripe Payment ID)

class RaceEntry(models.Model):
    # Correctly reference the 'Race' model from the 'event_management' app
    race = models.ForeignKey('event_management.Race', on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Other fields specific to a race entry

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Other product-specific fields
