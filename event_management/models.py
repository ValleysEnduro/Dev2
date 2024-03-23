from django.db import models
from treebeard.mp_tree import MP_Node

class Venue(MP_Node):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

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

    node_order_by = ['start_time']

    def __str__(self):
        return self.name

