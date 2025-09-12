import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'sittirat'
new_password = 'Sittiratsp2412'

u = User.objects.filter(username=username).first()
if not u:
    print('user_not_found')
else:
    u.set_password(new_password)
    u.save()
    print('password_set', username)
