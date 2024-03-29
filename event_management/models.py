from django.db import models
from treebeard.mp_tree import MP_Node
from age_categories.models import AgeCategory  # Import the AgeCategory model

class Venue(MP_Node):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    node_order_by = ['name']

    def __str__(self):
        return self.name

class Event(MP_Node):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    date = models.DateField()

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

