import os
import sys
from django.core.wsgi import get_wsgi_application

sys.stdout.write("WSGI application module loaded.\n")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbe.settings')

application = get_wsgi_application()
sys.stdout.write("WSGI application set.\n")
