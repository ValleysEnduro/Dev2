from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

class PostAdmin(SummernoteModelAdmin):  # Inherit from SummernoteModelAdmin
    list_display = ('title', 'subtitle', 'author', 'created_on')
    search_fields = ('title', 'subtitle', 'body')
    prepopulated_fields = {'seo_title': ('title',), 'seo_meta_description': ('subtitle',)}
    summernote_fields = ('content',)  # Specify fields to use Summernote

admin.site.register(Post, PostAdmin)