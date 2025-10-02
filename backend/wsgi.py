"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Set the settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Django
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

# For Vercel deployment - these variables must be at module level
app = application
handler = application

# Auto-migrate for Vercel
if os.environ.get('VERCEL_ENV'):
    try:
        from django.core.management import call_command
        call_command('migrate', run_syncdb=True, verbosity=0, interactive=False)
    except Exception:
        pass
