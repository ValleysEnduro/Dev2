from django.db import models
from treebeard.mp_tree import MP_Node
from age_categories.models import AgeCategory  # Import the AgeCategory model
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from django.conf import settings

class Venue(MP_Node):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    hero_image = ProcessedImageField(upload_to='venues/',
                                     processors=[ResizeToFill(1024, 768)],
                                     format='WEBP',
                                     options={'quality': 90},
                                     blank=True,
                                     null=True)

    node_order_by = ['name']

    def __str__(self):
        return self.name

class Event(MP_Node):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    description = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    node_order_by = ['date']

    def __str__(self):
        return self.name

class Race(MP_Node):
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    start_time = models.TimeField()
    age_categories = models.ManyToManyField(AgeCategory, related_name='races', blank=True)  # Add this line

    node_order_by = ['start_time']

    def __str__(self):
        return self.name

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='entries')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age_category = models.ForeignKey(AgeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    club_team_name = models.CharField(max_length=100, blank=True)
    entry_close_datetime = models.DateTimeField()
    transfer_close_datetime = models.DateTimeField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.race.name}"

    @property
    def can_edit_or_transfer(self):
        """Check if the entry is within the editable or transferable period."""
        return timezone.now() < self.transfer_close_datetime