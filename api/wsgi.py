"""
WSGI config for backend project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Get the Django WSGI application
application = get_wsgi_application()

# Vercel needs a 'handler' function
def handler(request):
    """Handle Vercel serverless function requests."""
    return application(request)