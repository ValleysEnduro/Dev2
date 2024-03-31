from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=255)
    hero_image = models.ImageField(upload_to='venues/')
    location = models.CharField(max_length=255)

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    capacity = models.IntegerField()
    race_type = models.CharField(max_length=50)  # Example: Enduro, XC
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')

class Race(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    name = models.CharField(max_length=255)
    categories = models.JSONField()  # Stores categories like Men's Elite, Women's Open
    distance = models.DecimalField(max_digits=5, decimal_places=2)

class Participant(models.Model):
    races = models.ManyToManyField(Race, related_name='participants')
    name = models.CharField(max_length=255)
    team = models.CharField(max_length=255, null=True, blank=True)
    age_category = models.CharField(max_length=50)
