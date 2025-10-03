from django.http import JsonResponse
from django.urls import path

def hello_world(request):
    return JsonResponse({
        'message': 'Hello from Railway!',
        'status': 'success',
        'timestamp': '2025-10-03'
    })

urlpatterns = [
    path('', hello_world),
    path('api/', hello_world),
    path('admin/', hello_world),
]