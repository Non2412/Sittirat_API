from django.contrib import admin
from .models import TouristAttraction, Accommodation, TourPackage, Tourist, Booking, Review

@admin.register(TouristAttraction)
class TouristAttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'district', 'rating', 'entrance_fee', 'is_active', 'created_at']
    list_filter = ['category', 'district', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'district', 'subdistrict']
    list_editable = ['rating', 'entrance_fee', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('ที่อยู่', {
            'fields': ('district', 'subdistrict', 'address', 'latitude', 'longitude')
        }),
        ('ข้อมูลติดต่อ', {
            'fields': ('phone', 'website', 'opening_hours', 'entrance_fee')
        }),
        ('คะแนน', {
            'fields': ('rating',)
        }),
        ('วันที่', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'district', 'price_per_night', 'available_rooms', 'total_rooms', 'rating', 'is_active']
    list_filter = ['type', 'district', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'district']
    list_editable = ['price_per_night', 'available_rooms', 'rating', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'type', 'description', 'is_active')
        }),
        ('ที่อยู่และติดต่อ', {
            'fields': ('district', 'address', 'phone', 'email', 'website')
        }),
        ('ห้องพักและราคา', {
            'fields': ('total_rooms', 'available_rooms', 'price_per_night')
        }),
        ('เวลาและสิ่งอำนวยความสะดวก', {
            'fields': ('check_in_time', 'check_out_time', 'amenities')
        }),
        ('คะแนน', {
            'fields': ('rating',)
        }),
        ('วันที่', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'price_adult', 'price_child', 'max_participants', 'rating', 'is_active']
    list_filter = ['duration', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price_adult', 'price_child', 'max_participants', 'rating', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['attractions']
    
    fieldsets = (
        ('ข้อมูลทั่วไป', {
            'fields': ('name', 'description', 'duration', 'is_active')
        }),
        ('ราคาและจำนวนผู้เข้าร่วม', {
            'fields': ('price_adult', 'price_child', 'max_participants')
        }),
        ('บริการ', {
            'fields': ('included_services', 'excluded_services', 'meeting_point')
        }),
        ('สถานที่ในแพ็คเกจ', {
            'fields': ('attractions',)
        }),
        ('คะแนน', {
            'fields': ('rating',)
        }),
        ('วันที่', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('ข้อมูลผู้ใช้', {
            'fields': ('user',)
        }),
        ('ข้อมูลติดต่อ', {
            'fields': ('phone', 'id_card', 'address')
        }),
        ('ติดต่อฉุกเฉิน', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('วันที่', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking_type', 'tourist', 'get_booked_item', 'total_amount', 'status', 'created_at']
    list_filter = ['booking_type', 'status', 'created_at']
    search_fields = ['tourist__user__username', 'accommodation__name', 'tour_package__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_booked_item(self, obj):
        if obj.booking_type == 'accommodation':
            return obj.accommodation.name if obj.accommodation else '-'
        elif obj.booking_type == 'tour_package':
            return obj.tour_package.name if obj.tour_package else '-'
        return '-'
    get_booked_item.short_description = 'รายการที่จอง'
    
    fieldsets = (
        ('ข้อมูลการจอง', {
            'fields': ('booking_type', 'tourist', 'status', 'total_amount')
        }),
        ('การจองที่พัก', {
            'fields': ('accommodation', 'check_in_date', 'check_out_date', 'rooms'),
            'classes': ('collapse',)
        }),
        ('การจองทัวร์', {
            'fields': ('tour_package', 'tour_date', 'adults', 'children'),
            'classes': ('collapse',)
        }),
        ('ข้อมูลเพิ่มเติม', {
            'fields': ('special_requests',)
        }),
        ('วันที่', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['tourist', 'get_reviewed_item', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['tourist__user__username', 'attraction__name', 'accommodation__name', 'tour_package__name', 'comment']
    readonly_fields = ['created_at']
    
    def get_reviewed_item(self, obj):
        if obj.attraction:
            return f"สถานที่: {obj.attraction.name}"
        elif obj.accommodation:
            return f"ที่พัก: {obj.accommodation.name}"
        elif obj.tour_package:
            return f"ทัวร์: {obj.tour_package.name}"
        return '-'
    get_reviewed_item.short_description = 'รายการที่รีวิว'
    
    fieldsets = (
        ('ข้อมูลรีวิว', {
            'fields': ('tourist', 'rating', 'comment')
        }),
        ('รายการที่รีวิว', {
            'fields': ('attraction', 'accommodation', 'tour_package')
        }),
        ('วันที่', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )