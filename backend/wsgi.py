import os
import sys
import traceback

# Set the settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Add project root to Python path for Vercel
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from django.core.wsgi import get_wsgi_application
    
    # Create the WSGI application
    application = get_wsgi_application()
    
    # For Vercel deployment
    app = application
    handler = application

except Exception as e:
    # Create a simple error response app
    def error_application(environ, start_response):
        error_message = f"Django Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain; charset=utf-8'),
            ('Content-Length', str(len(error_message.encode('utf-8'))))
        ])
        return [error_message.encode('utf-8')]
    
    application = error_application
    app = error_application
    handler = error_application
