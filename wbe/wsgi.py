import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbe.settings')  # Ensure this matches your settings module

application = get_wsgi_application()
