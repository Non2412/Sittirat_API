from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .auth_serializers import register, login_view  

router = DefaultRouter()
router.register(r'attractions', views.TouristAttractionViewSet)
router.register(r'accommodations', views.AccommodationViewSet)
router.register(r'tour-packages', views.TourPackageViewSet)
router.register(r'tourists', views.TouristViewSet)
router.register(r'bookings', views.BookingViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Authentication URLs
    path('auth/register/', register, name='register'),
    path('auth/login/', login_view, name='login'),
    
    # Dashboard และสถิติ
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('dashboard/popular-destinations/', views.popular_destinations, name='popular-destinations'),
    path('dashboard/district-stats/', views.district_stats, name='district-stats'),
    path('dashboard/booking-trends/', views.booking_trends, name='booking-trends'),
    path('dashboard/accommodation-availability/', views.accommodation_availability, name='accommodation-availability'),
    path('dashboard/sisaket-highlights/', views.sisaket_highlights, name='sisaket-highlights'),
    
    # การจอง
    path('bookings/accommodation/create/', views.create_accommodation_booking, name='create-accommodation-booking'),
    path('bookings/tour/create/', views.create_tour_booking, name='create-tour-booking'),
]