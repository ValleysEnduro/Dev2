from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Venue, Event, Race, Entry
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

# Register Venue, Event, and Race with Treebeard's TreeAdmin
class VenueAdmin(TreeAdmin):
    form = movenodeform_factory(Venue)

class EventAdmin(TreeAdmin, SummernoteModelAdmin):  # Use both TreeAdmin and SummernoteModelAdmin
    form = movenodeform_factory(Event)
    summernote_fields = ('description',)  # Specify the Summernote field(s)

class RaceAdmin(TreeAdmin):
    form = movenodeform_factory(Race)

# Standard admin registration for Entry, as it's not using Treebeard
class EntryAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'race', 'user']
    search_fields = ['first_name', 'last_name', 'race__name', 'user__username']

admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Entry, EntryAdmin)
