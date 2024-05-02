from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import homepage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view, name='homepage'),  # This serves as the homepage
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('summernote/', include('django_summernote.urls')),
    path('core/', include(('core.urls', 'core'))),
    path('event_management/', include(('event_management.urls', 'event_management'), namespace='event_management')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    # Placeholder for future paths
    # path('events/', include('events.urls')),
    # Add other apps' URLs here...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
