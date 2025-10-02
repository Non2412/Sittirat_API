import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('VERCEL_ENV', 'production')

# Import Django
from django.core.wsgi import get_wsgi_application

# Create application
application = get_wsgi_application()

# For Vercel
app = application
handler = application

def handler(event, context):
    return application(event['environ'], event['start_response'])