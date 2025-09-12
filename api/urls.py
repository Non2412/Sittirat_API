from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TouristAttractionViewSet, AccommodationViewSet, TourPackageViewSet
from .auth_views import register, login_view


router = DefaultRouter()
router.register(r'attractions', TouristAttractionViewSet, basename='attraction')
router.register(r'accommodations', AccommodationViewSet, basename='accommodation')
router.register(r'tour-packages', TourPackageViewSet, basename='tourpackage')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='api-register'),
    path('login/', login_view, name='api-login'),
]
