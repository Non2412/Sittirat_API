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
test_passwords = ['SittiratAdmin2025!', 'Sittiratsp2412', 'sittirat']

u = User.objects.filter(username=username).first()
if not u:
    print('user_not_found')
else:
    print('username:', u.username)
    print('is_active:', u.is_active)
    print('is_staff:', u.is_staff)
    print('is_superuser:', u.is_superuser)
    print('password hash prefix:', u.password[:20])
    for p in test_passwords:
        print('check', p, '->', u.check_password(p))
