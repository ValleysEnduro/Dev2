from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Venue, Event, Race, Entry
from treebeard.admin import TreeAdmin
from django.contrib import admin
from django.db.models import Count, Prefetch, Q
from django.urls import reverse
from django.utils.html import format_html
from .models import Venue, Event, Race, Entry
from treebeard.admin import TreeAdmin
from django import forms


# Inline admin for Event in VenueAdmin
class EventInline(admin.StackedInline):
    model = Event
    extra = 0  # Adjust the number of empty forms

# Inline admin for Race in EventAdmin
class RaceInline(admin.TabularInline):
    model = Race
    extra = 1  # Adjust according to your needs

# Inline admin for Entry in RaceAdmin
class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1

# Admin class for Venue
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'view_total_events_link', 'view_total_races_link', 'view_total_entries_link')

    def view_total_events_link(self, obj):
        count = obj.events.count()
        url = reverse('admin:event_management_event_changelist') + f'?venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)
    view_total_events_link.short_description = 'Total Events'

    def view_total_races_link(self, obj):
        count = Race.objects.filter(event__venue=obj).count()
        url = reverse('admin:event_management_race_changelist') + f'?event__venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)
    view_total_races_link.short_description = 'Total Races'

    def view_total_entries_link(self, obj):
        count = Entry.objects.filter(race__event__venue=obj).count()
        url = reverse('admin:event_management_entry_changelist') + f'?race__event__venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)
    view_total_entries_link.short_description = 'Total Entries'
# Admin class for Event
class EventAdmin(TreeAdmin, admin.ModelAdmin):  # Note: TreeAdmin is used if you want to keep tree functionalities
    list_display = ('name', 'get_depth', 'get_numchild', 'get_numraces', 'get_numentries')
    exclude = ('path', 'depth', 'numchild')
    inlines = [RaceInline]

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

# Admin class for Race
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'view_entries_link',)
    inlines = [EntryInline]

    def view_entries_link(self, obj):
        url = reverse('admin:event_management_entry_changelist') + f'?race__id__exact={obj.pk}'
        return format_html('<a href="{}">View Entries</a>', url)
    view_entries_link.short_description = "Entries"

# EntryAdmin remains as you previously defined, no need for changes as it's the last level
class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'first_name', 'last_name', 'age_category', 'club_team_name', 'entry_close_datetime', 'transfer_close_datetime', 'is_archived',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'date')
    list_filter = ('venue', 'date')  # Filter by venue and date
    search_fields = ('name', 'description')  # Search by event name and description
    inlines = [RaceInline]

class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'start_time')
    list_filter = ('event', 'start_time')  # Filter by event and start time
    search_fields = ('name',)
    inlines = [EntryInline]

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['depth', 'numchild']  # Exclude system-managed fields

class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    readonly_fields = ('last_modified',)  # Example of making a field read-only
    inlines = [RaceInline]



# Registration of admin classes
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Entry, EntryAdmin)
