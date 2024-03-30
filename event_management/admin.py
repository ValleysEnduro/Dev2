from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Venue, Event, Race, Entry
from treebeard.admin import TreeAdmin
from treebeard.forms import MoveNodeForm

# Adjusted VenueAdmin for Treebeard
class VenueAdmin(TreeAdmin):
    form = MoveNodeForm
    # Define any additional fields or configurations here

# Adjusted EventAdmin to integrate Summernote without MPTTModelAdmin
class EventAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('description',)
    # Since Event is not using Treebeard for hierarchical features based on the model structure shared,
    # it's managed as a regular model but with Summernote integration for the description field.

# Standard admin registration for Race
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'start_time']
    search_fields = ['name', 'event__name']

# Standard admin registration for Entry
class EntryAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'race', 'user']
    search_fields = ['first_name', 'last_name', 'race__name', 'user__username']

admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Entry, EntryAdmin)
