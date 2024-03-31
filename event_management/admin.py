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
from django.db import transaction


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
# Updated Admin class for Event without TreeAdmin
class EventAdmin(admin.ModelAdmin):  # Removed TreeAdmin
    list_display = ('name', 'venue', 'date', 'view_total_races_link', 'view_total_entries_link')
    inlines = [RaceInline]

    def view_total_races_link(self, obj):
        count = obj.races.count()
        url = reverse('admin:event_management_race_changelist') + f'?event__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)
    view_total_races_link.short_description = "Total Races"

    def view_total_entries_link(self, obj):
        count = Entry.objects.filter(race__event=obj).count()
        url = reverse('admin:event_management_entry_changelist') + f'?race__event__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)
    view_total_entries_link.short_description = "Total Entries"

    @admin.action(description='Duplicate selected events and their races (without entries)')
    def duplicate_event(self, request, queryset):
        with transaction.atomic():
            for original_event in queryset:
                # Duplicate the event instance
                original_event_id = original_event.id
                original_event.pk = None
                original_event.name += " (Copy)"
                original_event.is_completed = False  # Assuming is_completed field exists
                original_event.save()

                # Duplicate races associated with the original event, without duplicating entries
                races = Race.objects.filter(event_id=original_event_id)
                for race in races:
                    race.pk = None
                    race.event = original_event  # Link to the newly created event
                    race.save()
                    # Note: This process doesn't duplicate entries associated with each race.

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
    list_display = ('user', 'race', 'first_name', 'last_name', 'age_category', 'club_team_name', 'is_archived',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'date')
    list_filter = ('venue', 'date')  # Filter by venue and date
    search_fields = ('name', 'description')  # Search by event name and description
    inlines = [RaceInline]

class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'start_time', 'entry_close_datetime', 'transfer_close_datetime',)
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
