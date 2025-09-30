from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Sum, Avg, QuerySet
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models import F, ExpressionWrapper, FloatField
from .models import TouristAttraction, Accommodation, TourPackage, Tourist, Booking, Review
from .serializers import (
    TouristAttractionSerializer, TouristAttractionSummarySerializer,
    AccommodationSerializer, AccommodationSummarySerializer,
    TourPackageSerializer, TourPackageSummarySerializer,
    TouristSerializer, BookingSerializer, ReviewSerializer
)


class TouristAttractionViewSet(viewsets.ModelViewSet):
    queryset = TouristAttraction.objects.all()
    serializer_class = TouristAttractionSerializer
    permission_classes = [AllowAny]  # เปิดให้ดูได้ทุกคน

    def get_serializer_class(self):
        if self.action == 'list':
            return TouristAttractionSummarySerializer
        return TouristAttractionSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """ค้นหาสถานที่ท่องเที่ยว"""
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        district = request.query_params.get('district', '')
        min_rating = request.query_params.get('min_rating', 0)

        attractions = TouristAttraction.objects.filter(is_active=True)

        # ✅ ไม่ใช้ Q object - ใช้การ filter หลายครั้งแทน
        if query:
            # สร้าง queryset ว่างเพื่อรวมผลลัพธ์
            filtered_attractions = TouristAttraction.objects.none()
            
            # ค้นหาในแต่ละ field แล้วรวมกัน (OR logic)
            filtered_attractions = filtered_attractions | attractions.filter(name__icontains=query)
            filtered_attractions = filtered_attractions | attractions.filter(description__icontains=query)
            filtered_attractions = filtered_attractions | attractions.filter(district__icontains=query)
            filtered_attractions = filtered_attractions | attractions.filter(subdistrict__icontains=query)
            
            attractions = filtered_attractions.distinct()

        if category:
            attractions = attractions.filter(category=category)

        if district:
            attractions = attractions.filter(district__icontains=district)

        if min_rating:
            attractions = attractions.filter(rating__gte=float(min_rating))

        serializer = TouristAttractionSummarySerializer(attractions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """ดึงหมวดหมู่สถานที่ท่องเที่ยวทั้งหมด"""
        categories = [{'value': choice[0], 'label': choice[1]}
                      for choice in TouristAttraction.CATEGORY_CHOICES]
        return Response(categories)

    @action(detail=False, methods=['get'])
    def districts(self, request):
        """ดึงอำเภอทั้งหมดในศรีสะเกษ"""
        districts = TouristAttraction.objects.values_list(
            'district', flat=True).distinct().order_by('district')
        return Response(list(districts))

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """สถานที่ท่องเที่ยวยอดนิยม (คะแนนสูง)"""
        attractions = TouristAttraction.objects.filter(
            is_active=True, rating__gte=4.0).order_by('-rating')[:10]
        serializer = TouristAttractionSummarySerializer(attractions, many=True)
        return Response(serializer.data)


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AccommodationSummarySerializer
        return AccommodationSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """ค้นหาที่พัก"""
        query = request.query_params.get('q', '')
        type_filter = request.query_params.get('type', '')
        district = request.query_params.get('district', '')
        max_price = request.query_params.get('max_price', '')
        min_rating = request.query_params.get('min_rating', 0)

        accommodations = Accommodation.objects.filter(
            is_active=True, available_rooms__gt=0)

        # ✅ ไม่ใช้ Q object
        if query:
            filtered_accommodations = Accommodation.objects.none()
            
            filtered_accommodations = filtered_accommodations | accommodations.filter(name__icontains=query)
            filtered_accommodations = filtered_accommodations | accommodations.filter(description__icontains=query)
            filtered_accommodations = filtered_accommodations | accommodations.filter(district__icontains=query)
            
            accommodations = filtered_accommodations.distinct()

        if type_filter:
            accommodations = accommodations.filter(type=type_filter)

        if district:
            accommodations = accommodations.filter(
                district__icontains=district)

        if max_price:
            accommodations = accommodations.filter(
                price_per_night__lte=float(max_price))

        if min_rating:
            accommodations = accommodations.filter(
                rating__gte=float(min_rating))

        serializer = AccommodationSummarySerializer(accommodations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def types(self, request):
        """ดึงประเภทที่พักทั้งหมด"""
        types = [{'value': choice[0], 'label': choice[1]}
                 for choice in Accommodation.TYPE_CHOICES]
        return Response(types)


class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TourPackageSummarySerializer
        return TourPackageSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """ค้นหาแพ็คเกจทัวร์"""
        query = request.query_params.get('q', '')
        duration = request.query_params.get('duration', '')
        max_price = request.query_params.get('max_price', '')
        min_rating = request.query_params.get('min_rating', 0)

        packages = TourPackage.objects.filter(is_active=True)

        # ✅ ไม่ใช้ Q object
        if query:
            filtered_packages = TourPackage.objects.none()
            
            filtered_packages = filtered_packages | packages.filter(name__icontains=query)
            filtered_packages = filtered_packages | packages.filter(description__icontains=query)
            
            packages = filtered_packages.distinct()

        if duration:
            packages = packages.filter(duration=duration)

        if max_price:
            packages = packages.filter(price_adult__lte=float(max_price))

        if min_rating:
            packages = packages.filter(rating__gte=float(min_rating))

        serializer = TourPackageSummarySerializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def durations(self, request):
        """ดึงระยะเวลาแพ็คเกจทั้งหมด"""
        durations = [{'value': choice[0], 'label': choice[1]}
                     for choice in TourPackage.DURATION_CHOICES]
        return Response(durations)


class TouristViewSet(viewsets.ModelViewSet):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # ต้อง login ก่อน

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """อัปเดตสถานะการจอง"""
        booking = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Booking.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = new_status
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_tourist(self, request):
        """ดึงการจองของนักท่องเที่ยวคนใดคนหนึ่ง"""
        tourist_id = request.query_params.get('tourist_id')
        if not tourist_id:
            return Response({'error': 'tourist_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(
            tourist_id=tourist_id).order_by('-created_at')
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=['get'])
    def by_attraction(self, request):
        """ดึงรีวิวของสถานที่ท่องเที่ยว"""
        attraction_id = request.query_params.get('attraction_id')
        if not attraction_id:
            return Response({'error': 'attraction_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(
            attraction_id=attraction_id).order_by('-created_at')
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_accommodation(self, request):
        """ดึงรีวิวของที่พัก"""
        accommodation_id = request.query_params.get('accommodation_id')
        if not accommodation_id:
            return Response({'error': 'accommodation_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        reviews = Review.objects.filter(
            accommodation_id=accommodation_id).order_by('-created_at')
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

# Function-based views สำหรับสถิติและรายงาน


@api_view(['GET'])
def dashboard_stats(request):
    """สถิติสำหรับ Dashboard"""
    stats = {
        'total_attractions': TouristAttraction.objects.filter(is_active=True).count(),
        'total_accommodations': Accommodation.objects.filter(is_active=True).count(),
        'total_tour_packages': TourPackage.objects.filter(is_active=True).count(),
        'total_bookings': Booking.objects.count(),
        'total_revenue': Booking.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        'average_accommodation_rating': Accommodation.objects.filter(is_active=True).aggregate(avg=Avg('rating'))['avg'] or 0,
        'average_tour_package_rating': TourPackage.objects.filter(is_active=True).aggregate(avg=Avg('rating'))['avg'] or 0,
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
        'paid_bookings': Booking.objects.filter(status='paid').count(),
        'completed_bookings': Booking.objects.filter(status='completed').count(),
        'cancelled_bookings': Booking.objects.filter(status='cancelled').count(),
    }
    return Response(stats)


@api_view(['GET'])
def popular_destinations(request):
    """สถานที่ท่องเที่ยวยอดนิยม"""
    limit = int(request.query_params.get('limit', 10))
    attractions = TouristAttraction.objects.filter(
        is_active=True,
        rating__gte=4.0
    ).order_by('-rating')[:limit]

    serializer = TouristAttractionSummarySerializer(attractions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def district_stats(request):
    """สถิติแยกตามอำเภอ"""
    from django.db.models import Count

    stats = TouristAttraction.objects.values('district').annotate(
        attraction_count=Count('id')
    ).order_by('-attraction_count')

    # เพิ่มข้อมูลที่พัก
    for stat in stats:
        district = stat['district']
        stat['accommodation_count'] = Accommodation.objects.filter(
            district=district).count()

    return Response(stats)


@api_view(['GET'])
def booking_trends(request):
    """แนวโน้มการจอง"""
    days = int(request.query_params.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)

    # Use TruncDate for database-agnostic date truncation
    bookings = (
        Booking.objects.filter(created_at__date__range=[start_date, end_date])
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'), revenue=Sum('total_amount'))
        .order_by('day')
    )

    return Response(list(bookings))


@api_view(['GET'])
def accommodation_availability(request):
    """ความพร้อมใช้งานของที่พัก"""
    district = request.query_params.get('district', '')

    accommodations = Accommodation.objects.filter(is_active=True)

    if district:
        accommodations = accommodations.filter(district__icontains=district)

    # Compute occupancy_rate per accommodation using F expressions and cast to float
    occupancy_expr = ExpressionWrapper(
        (F('total_rooms') - F('available_rooms')) * 100.0 / F('total_rooms'),
        output_field=FloatField()
    )

    data = (
        accommodations.annotate(occupancy_rate=occupancy_expr)
        .values('name', 'district', 'total_rooms', 'available_rooms', 'occupancy_rate')
    )

    return Response(list(data))


@api_view(['POST'])
def create_accommodation_booking(request):
    """สร้างการจองที่พัก"""
    try:
        tourist_id = request.data.get('tourist_id')
        accommodation_id = request.data.get('accommodation_id')
        check_in_date = request.data.get('check_in_date')
        check_out_date = request.data.get('check_out_date')
        rooms = int(request.data.get('rooms', 1))
        special_requests = request.data.get('special_requests', '')

        if not all([tourist_id, accommodation_id, check_in_date, check_out_date]):
            return Response(
                {'error': 'tourist_id, accommodation_id, check_in_date, check_out_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        tourist = Tourist.objects.get(id=tourist_id)
        accommodation = Accommodation.objects.get(id=accommodation_id)

        # ตรวจสอบความพร้อมใช้งาน
        if accommodation.available_rooms < rooms:
            return Response(
                {'error': f'ห้องว่างไม่เพียงพอ (ห้องว่าง: {accommodation.available_rooms})'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # คำนวดจำนวนคืน
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        nights = (check_out - check_in).days

        if nights <= 0:
            return Response(
                {'error': 'วันเช็คอินต้องมาก่อนวันเช็คเอาท์'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = accommodation.price_per_night * rooms * nights

        # สร้างการจอง
        booking = Booking.objects.create(
            booking_type='accommodation',
            tourist=tourist,
            accommodation=accommodation,
            check_in_date=check_in,
            check_out_date=check_out,
            rooms=rooms,
            total_amount=total_amount,
            special_requests=special_requests
        )

        # อัปเดตห้องว่าง
        accommodation.available_rooms -= rooms
        accommodation.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Tourist.DoesNotExist:
        return Response(
            {'error': 'Tourist not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Accommodation.DoesNotExist:
        return Response(
            {'error': 'Accommodation not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def create_tour_booking(request):
    """สร้างการจองแพ็คเกจทัวร์"""
    try:
        tourist_id = request.data.get('tourist_id')
        tour_package_id = request.data.get('tour_package_id')
        tour_date = request.data.get('tour_date')
        adults = int(request.data.get('adults', 0))
        children = int(request.data.get('children', 0))
        special_requests = request.data.get('special_requests', '')

        if not all([tourist_id, tour_package_id, tour_date, adults]):
            return Response(
                {'error': 'tourist_id, tour_package_id, tour_date, adults are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        tourist = Tourist.objects.get(id=tourist_id)
        tour_package = TourPackage.objects.get(id=tour_package_id)

        total_participants = adults + children

        # ตรวจสอบจำนวนผู้เข้าร่วม
        if total_participants > tour_package.max_participants:
            return Response(
                {'error': f'จำนวนผู้เข้าร่วมเกินกำหนด (สูงสุด: {tour_package.max_participants})'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # คำนวดราคา
        total_amount = (tour_package.price_adult * adults) + \
            (tour_package.price_child * children)

        # สร้างการจอง
        booking = Booking.objects.create(
            booking_type='tour_package',
            tourist=tourist,
            tour_package=tour_package,
            tour_date=datetime.strptime(tour_date, '%Y-%m-%d').date(),
            adults=adults,
            children=children,
            total_amount=total_amount,
            special_requests=special_requests
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Tourist.DoesNotExist:
        return Response(
            {'error': 'Tourist not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except TourPackage.DoesNotExist:
        return Response(
            {'error': 'Tour package not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def sisaket_highlights(request):
    """ไhighlight สถานที่ท่องเที่ยวที่น่าสนใจในศรีสะเกษ"""
    highlights = {
        'historical_sites': TouristAttraction.objects.filter(
            category='historical',
            is_active=True
        ).order_by('-rating')[:5],
        'temples': TouristAttraction.objects.filter(
            category='temple',
            is_active=True
        ).order_by('-rating')[:5],
        'natural_attractions': TouristAttraction.objects.filter(
            category='natural',
            is_active=True
        ).order_by('-rating')[:5],
        'cultural_sites': TouristAttraction.objects.filter(
            category='cultural',
            is_active=True
        ).order_by('-rating')[:5],
    }

    response_data = {}
    for key, queryset in highlights.items():
        response_data[key] = TouristAttractionSummarySerializer(
            queryset, many=True).data

    return Response(response_data)