from django.contrib import admin
import nested_admin
from .models import Venue, Event, Race

class RaceInline(nested_admin.NestedTabularInline):
    model = Race
    extra = 1

class EventInline(nested_admin.NestedTabularInline):
    model = Event
    inlines = [RaceInline]
    extra = 1

class VenueAdmin(nested_admin.NestedModelAdmin):
    inlines = [EventInline]
    list_display = ('name', 'location')

admin.site.register(Venue, VenueAdmin)
