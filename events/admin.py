from django.contrib import admin
from django.utils import timezone
from .models import Event, Venue, Race, Participant

# Inline admin for Races within an Event
class RaceInline(admin.TabularInline):
    model = Race
    extra = 1  # How many extra forms to show

# Custom filter for filtering events by date
class EventDateFilter(admin.SimpleListFilter):
    title = 'event date'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('upcoming', 'Upcoming'),
            ('past', 'Past'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'upcoming':
            return queryset.filter(date__gte=timezone.now())
        if self.value() == 'past':
            return queryset.filter(date__lt=timezone.now())

# Admin model for Event, including the RaceInline and EventDateFilter
class EventAdmin(admin.ModelAdmin):
    inlines = [RaceInline]
    list_filter = (EventDateFilter,)

# Registering models with the admin site
admin.site.register(Event, EventAdmin)
admin.site.register(Venue)
admin.site.register(Participant)
