import os
import sys

# Ensure project root is on path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'sittirat'
email = 'sittirat@example.com'
password = 'SittiratAdmin2025!'

u = User.objects.filter(username=username).first()
if u:
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.is_active = True
    u.save()
    print('updated', username)
else:
    User.objects.create_superuser(username, email, password)
    print('created', username)
