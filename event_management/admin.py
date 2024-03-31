from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Venue, Event, Race, Entry
from django_summernote.admin import SummernoteModelAdmin, SummernoteInlineModelAdmin
from django import forms
from django.db import transaction
import csv
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entries.csv"'
    writer = csv.writer(response)

    writer.writerow(['First Name', 'Last Name', 'Email', 'Race', 'Age Category'])
    for entry in queryset:
        writer.writerow([
            entry.first_name,
            entry.last_name,
            entry.email,
            entry.race.name,
            entry.age_category.name if entry.age_category else ''
        ])

    return response

export_as_csv.short_description = "Export Selected Entries as CSV"

# Inline admin for Event in VenueAdmin
class EventInline(SummernoteInlineModelAdmin, admin.StackedInline):  # Use SummernoteInlineModelAdmin for rich text
    model = Event
    extra = 0
    summernote_fields = ('description',)  # Apply Summernote to the description field

# Inline admin for Race in EventAdmin
class RaceInline(admin.TabularInline):
    model = Race
    extra = 1

# Inline admin for Entry in RaceAdmin
class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1

# Admin class for Venue
class VenueAdmin(SummernoteModelAdmin):  # Use SummernoteModelAdmin for rich text
    summernote_fields = ('description',)
    list_display = ('name', 'location', 'view_total_events_link', 'view_total_races_link', 'view_total_entries_link')
    inlines = [EventInline]  # Include EventInline here

    def view_total_events_link(self, obj):
        count = obj.events.count()
        url = reverse('admin:event_management_event_changelist') + f'?venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    def view_total_races_link(self, obj):
        count = Race.objects.filter(event__venue=obj).count()
        url = reverse('admin:event_management_race_changelist') + f'?event__venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    def view_total_entries_link(self, obj):
        count = Entry.objects.filter(race__event__venue=obj).count()
        url = reverse('admin:event_management_entry_changelist') + f'?race__event__venue__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    # Methods for creating view links remain unchanged

# Admin class for Event
class EventAdmin(SummernoteModelAdmin):  # Use SummernoteModelAdmin for rich text
    summernote_fields = ('description',)
    list_display = ('name', 'venue', 'date', 'view_total_races_link', 'view_total_entries_link')
    inlines = [RaceInline]  # Include RaceInline here

    def view_total_races_link(self, obj):
        count = obj.races.count()
        url = reverse('admin:event_management_race_changelist') + f'?event__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    def view_total_entries_link(self, obj):
        count = Entry.objects.filter(race__event=obj).count()
        url = reverse('admin:event_management_entry_changelist') + f'?race__event__id__exact={obj.pk}'
        return format_html('<a href="{}">{}</a>', url, count)

    # Methods for creating view links and duplicate events action remain unchanged

# Admin class for Race
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'view_entries_link',)
    inlines = [EntryInline]  # Include EntryInline here

    def view_entries_link(self, obj):
        url = reverse('admin:event_management_entry_changelist') + f'?race__id__exact={obj.pk}'
        return format_html('<a href="{}">View Entries</a>', url)

    # Method for creating view entries link remains unchanged

# Admin class for Entry remains as previously defined, no need for changes
class EntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'first_name', 'last_name', 'age_category', 'club_team_name', 'is_archived',)
    actions = [export_as_csv]

# Registration of admin classes
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Entry, EntryAdmin)



