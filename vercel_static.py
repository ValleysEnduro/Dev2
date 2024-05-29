import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbe.settings')
application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(settings.BASE_DIR, 'staticfiles'))
application.add_files(os.path.join(settings.BASE_DIR, 'static'), prefix='static/')
