
from django.contrib import admin
import nested_admin
from .models import Venue, Event, Race
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

# Assuming Venue, Event, and Race have the Tree structure from treebeard

class RaceInline(nested_admin.NestedTabularInline):
    model = Race
    extra = 1

class EventInline(nested_admin.NestedTabularInline):
    model = Event
    inlines = [RaceInline]
    extra = 1

class VenueAdmin(nested_admin.NestedModelAdmin, TreeAdmin):
    form = movenodeform_factory(Venue)
    inlines = [EventInline]
    list_display = ('name', 'location', 'display_depth', 'display_numchild')

    def display_depth(self, obj):
        return obj.depth
    display_depth.short_description = 'Hierarchy Level'

    def display_numchild(self, obj):
        return obj.numchild
    display_numchild.short_description = 'Number of Children'

class RaceInline(nested_admin.NestedTabularInline):
    model = Race
    form = movenodeform_factory(Race)  # Added to incorporate treebeard form functionality
    extra = 1
    readonly_fields = ('display_path', 'display_depth', 'display_numchild')  # New

    def display_path(self, obj):
        return obj.path
    display_path.short_description = 'Race Location Path'

    def display_depth(self, obj):
        return obj.depth
    display_depth.short_description = 'Race Hierarchy Level'

    def display_numchild(self, obj):
        return obj.numchild
    display_numchild.short_description = 'Number of Child Races'

class EventInline(nested_admin.NestedTabularInline):
    model = Event
    form = movenodeform_factory(Event)  # Added to incorporate treebeard form functionality
    inlines = [RaceInline]
    extra = 1
    readonly_fields = ('display_path', 'display_depth', 'display_numchild')  # New

    def display_path(self, obj):
        return obj.path
    display_path.short_description = 'Event Location Path'

    def display_depth(self, obj):
        return obj.depth
    display_depth.short_description = 'Event Hierarchy Level'

    def display_numchild(self, obj):
        return obj.numchild
    display_numchild.short_description = 'Number of Child Events'

class VenueAdmin(nested_admin.NestedModelAdmin):
    inlines = [EventInline]
    list_display = ('name', 'location')

admin.site.register(Venue, VenueAdmin)

# Repeat similar custom admin classes for Event and Race if they are MP_Node and need admin representation
