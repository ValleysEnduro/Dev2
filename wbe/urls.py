from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from core.views import homepage_view
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

]

# mysite/urls.py
# Assuming homepage_view is defined in core.views

urlpatterns = [
    path('', homepage_view, name='homepage'),  # This serves as the homepage
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('summernote/', include('django_summernote.urls')),
    # Placeholder for when you're ready to add events
    # path('events/', include('events.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    