from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Venue, Event, Race, Entry  # Removed trailing comma
from treebeard.admin import TreeAdmin
from django_summernote.admin import SummernoteModelAdmin  # Added missing import

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_events_link',)

    def view_events_link(self, obj):
        url = reverse('admin:event_management_event_changelist') + f'?venue__id__exact={obj.pk}'
        return format_html('<a href="{}">View Events</a>', url)

    view_events_link.short_description = "Events"

admin.site.register(Venue, VenueAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_depth', 'get_numchild', 'get_numraces', 'get_numentries')
    exclude = ('path', 'depth', 'numchild')

    def get_depth(self, obj):
        return f"Level {obj.depth} in the tree"
    get_depth.short_description = "Depth"

    def get_numchild(self, obj):
        return f"{obj.numchild} immediate children"
    get_numchild.short_description = "Number of Children"

    def get_numraces(self, obj):
        return obj.races.count()
    get_numraces.short_description = "Number of Races"

    def get_numentries(self, obj):
        return Entry.objects.filter(race__event=obj).count()
    get_numentries.short_description = "Number of Entries"

admin.site.register(Event, EventAdmin)

class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'view_entries_link',)  # Corrected from view_participants_link to view_entries_link

    def view_entries_link(self, obj):  # Renamed method
        url = reverse('admin:event_management_entry_changelist') + f'?race__id__exact={obj.pk}'
        return format_html('<a href="{}">View Entries</a>', url)

    view_entries_link.short_description = "Entries"

admin.site.register(Race, RaceAdmin)

# Renamed from ParticipantAdmin to EntryAdmin to match your model name
class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'first_name', 'last_name', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime', 'is_archived',)
    # Updated list_display to match the Entry model fields

admin.site.register(Entry, EntryAdmin)
