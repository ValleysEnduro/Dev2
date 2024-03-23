from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'author', 'created_on')
    search_fields = ('title', 'subtitle', 'body')
    prepopulated_fields = {'seo_title': ('title',), 'seo_meta_description': ('subtitle',)}

admin.site.register(Post, PostAdmin)