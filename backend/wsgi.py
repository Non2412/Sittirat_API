"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Vercel specific configuration
if os.environ.get('VERCEL_ENV'):
    # Add the project root to Python path
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Import Django and create WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    from django.core.management import call_command
    
    # Get the application
    application = get_wsgi_application()
    
    # Vercel needs these variable names
    app = application
    handler = application
    
    # Run migrations only in Vercel environment
    if os.environ.get('VERCEL_ENV'):
        try:
            call_command('migrate', verbosity=0, interactive=False)
        except Exception:
            # Ignore migration errors in serverless
            pass
            
except Exception as e:
    # Fallback for import errors
    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f'Django import error: {str(e)}'.encode('utf-8')]
    
    app = application
    handler = application
