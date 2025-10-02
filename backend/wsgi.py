"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Vercel environment detection and configuration
if os.environ.get('VERCEL_ENV'):
    # Set environment variables for Vercel
    os.environ.setdefault('VERCEL', '1')
    os.environ.setdefault('DEBUG', 'False')
    
    # Add the project directory to Python path for Vercel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create the WSGI application
application = get_wsgi_application()

# Vercel requires 'handler' or 'app' variable
handler = application
app = application

# Auto-migrate for Vercel (since it's stateless)
if os.environ.get('VERCEL_ENV'):
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    except Exception as e:
        # Ignore migration errors in serverless environment
        pass

# For Vercel deployment
app = application
