from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TouristAttraction, Accommodation, TourPackage, Tourist, Booking, Review


class TouristAttractionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TouristAttraction
        fields = '__all__'

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("คะแนนต้องอยู่ระหว่าง 0-5")
        return value


class TouristAttractionSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลสถานที่ท่องเที่ยวแบบย่อ"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TouristAttraction
        fields = ['id', 'name', 'category', 'category_display', 'district', 'rating', 'entrance_fee', 'is_active']


class AccommodationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Accommodation
        fields = '__all__'

    def validate_available_rooms(self, value):
        if value < 0:
            raise serializers.ValidationError("จำนวนห้องว่างต้องไม่ติดลบ")
        return value

    def validate(self, data):
        if data.get('available_rooms', 0) > data.get('total_rooms', 0):
            raise serializers.ValidationError("ห้องว่างต้องไม่เกินจำนวนห้องทั้งหมด")
        return data


class AccommodationSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลที่พักแบบย่อ"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'type', 'type_display', 'district', 'price_per_night', 'available_rooms', 'rating', 'is_active']


class TourPackageSerializer(serializers.ModelSerializer):
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    attractions = TouristAttractionSummarySerializer(many=True, read_only=True)
    attraction_ids = serializers.PrimaryKeyRelatedField(
        queryset=TouristAttraction.objects.all(),
        many=True,
        write_only=True,
        source='attractions'
    )

    class Meta:
        model = TourPackage
        fields = '__all__'


class TourPackageSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลแพ็คเกจทัวร์แบบย่อ"""
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)

    class Meta:
        model = TourPackage
        fields = ['id', 'name', 'duration', 'duration_display', 'price_adult', 'price_child', 'max_participants', 'rating', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tourist
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tourist_name = serializers.CharField(source='tourist.user.get_full_name', read_only=True)
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    tour_package_name = serializers.CharField(source='tour_package.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        booking_type = data.get('booking_type')

        if booking_type == 'accommodation':
            if not data.get('accommodation') or not data.get('check_in_date') or not data.get('check_out_date'):
                raise serializers.ValidationError("การจองที่พักต้องระบุที่พัก วันเช็คอิน และวันเช็คเอาท์")

            if data.get('check_in_date') >= data.get('check_out_date'):
                raise serializers.ValidationError("วันเช็คอินต้องมาก่อนวันเช็คเอาท์")

        elif booking_type == 'tour_package':
            if not data.get('tour_package') or not data.get('tour_date') or not data.get('adults'):
                raise serializers.ValidationError("การจองทัวร์ต้องระบุแพ็คเกจทัวร์ วันทัวร์ และจำนวนผู้ใหญ่")

        return data


class ReviewSerializer(serializers.ModelSerializer):
    tourist_name = serializers.CharField(source='tourist.user.get_full_name', read_only=True)
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    tour_package_name = serializers.CharField(source='tour_package.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        # ต้องระบุอย่างน้อย 1 ใน 3: attraction, accommodation, หรือ tour_package
        if not any([data.get('attraction'), data.get('accommodation'), data.get('tour_package')]):
            raise serializers.ValidationError("ต้องระบุสถานที่ท่องเที่ยว ที่พัก หรือแพ็คเกจทัวร์อย่างน้อย 1 อย่าง")

        return data


# Serializers สำหรับสถิติและรายงาน
class DistrictStatsSerializer(serializers.Serializer):
    district = serializers.CharField()
    attraction_count = serializers.IntegerField()
    accommodation_count = serializers.IntegerField()


class BookingStatsSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    accommodation_bookings = serializers.IntegerField()
    tour_bookings = serializers.IntegerField()
    pending_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TouristAttraction, Accommodation, TourPackage, Tourist, Booking, Review


class TouristAttractionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TouristAttraction
        fields = '__all__'

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("คะแนนต้องอยู่ระหว่าง 0-5")
        return value


class TouristAttractionSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลสถานที่ท่องเที่ยวแบบย่อ"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TouristAttraction
        fields = ['id', 'name', 'category', 'category_display', 'district', 'rating', 'entrance_fee', 'is_active']


class AccommodationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Accommodation
        fields = '__all__'

    def validate_available_rooms(self, value):
        if value < 0:
            raise serializers.ValidationError("จำนวนห้องว่างต้องไม่ติดลบ")
        return value

    def validate(self, data):
        if data.get('available_rooms', 0) > data.get('total_rooms', 0):
            raise serializers.ValidationError("ห้องว่างต้องไม่เกินจำนวนห้องทั้งหมด")
        return data


class AccommodationSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลที่พักแบบย่อ"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'type', 'type_display', 'district', 'price_per_night', 'available_rooms', 'rating', 'is_active']


class TourPackageSerializer(serializers.ModelSerializer):
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)
    attractions = TouristAttractionSummarySerializer(many=True, read_only=True)
    attraction_ids = serializers.PrimaryKeyRelatedField(
        queryset=TouristAttraction.objects.all(),
        many=True,
        write_only=True,
        source='attractions'
    )

    class Meta:
        model = TourPackage
        fields = '__all__'


class TourPackageSummarySerializer(serializers.ModelSerializer):
    """สำหรับแสดงข้อมูลแพ็คเกจทัวร์แบบย่อ"""
    duration_display = serializers.CharField(source='get_duration_display', read_only=True)

    class Meta:
        model = TourPackage
        fields = ['id', 'name', 'duration', 'duration_display', 'price_adult', 'price_child', 'max_participants', 'rating', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tourist
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tourist_name = serializers.CharField(source='tourist.user.get_full_name', read_only=True)
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    tour_package_name = serializers.CharField(source='tour_package.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        booking_type = data.get('booking_type')

        if booking_type == 'accommodation':
            if not data.get('accommodation') or not data.get('check_in_date') or not data.get('check_out_date'):
                raise serializers.ValidationError("การจองที่พักต้องระบุที่พัก วันเช็คอิน และวันเช็คเอาท์")

            if data.get('check_in_date') >= data.get('check_out_date'):
                raise serializers.ValidationError("วันเช็คอินต้องมาก่อนวันเช็คเอาท์")

        elif booking_type == 'tour_package':
            if not data.get('tour_package') or not data.get('tour_date') or not data.get('adults'):
                raise serializers.ValidationError("การจองทัวร์ต้องระบุแพ็คเกจทัวร์ วันทัวร์ และจำนวนผู้ใหญ่")

        return data


class ReviewSerializer(serializers.ModelSerializer):
    tourist_name = serializers.CharField(source='tourist.user.get_full_name', read_only=True)
    attraction_name = serializers.CharField(source='attraction.name', read_only=True)
    accommodation_name = serializers.CharField(source='accommodation.name', read_only=True)
    tour_package_name = serializers.CharField(source='tour_package.name', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        # ต้องระบุอย่างน้อย 1 ใน 3: attraction, accommodation, หรือ tour_package
        if not any([data.get('attraction'), data.get('accommodation'), data.get('tour_package')]):
            raise serializers.ValidationError("ต้องระบุสถานที่ท่องเที่ยว ที่พัก หรือแพ็คเกจทัวร์อย่างน้อย 1 อย่าง")

        return data


# Serializers สำหรับสถิติและรายงาน
class DistrictStatsSerializer(serializers.Serializer):
    district = serializers.CharField()
    attraction_count = serializers.IntegerField()
    accommodation_count = serializers.IntegerField()


class BookingStatsSerializer(serializers.Serializer):
    total_bookings = serializers.IntegerField()
    accommodation_bookings = serializers.IntegerField()
    tour_bookings = serializers.IntegerField()
    pending_bookings = serializers.IntegerField()
    confirmed_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
