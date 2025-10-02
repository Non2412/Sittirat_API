#!/usr/bin/env python
"""
Build script for Vercel deployment.
This script runs during the build phase to set up the database.
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.environ.setdefault('VERCEL_ENV', 'production')
    
    django.setup()
    
    try:
        # Create database tables
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("Database migration completed successfully")
    except Exception as e:
        print(f"Migration warning: {e}")
        # Continue anyway for serverless environment
        pass