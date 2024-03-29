# age_categories/admin.py

from django.contrib import admin
from .models import AgeCategory

@admin.register(AgeCategory)
class AgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'min_age', 'max_age')
