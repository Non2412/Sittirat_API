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

application = get_wsgi_application()

# For Vercel deployment
app = application
