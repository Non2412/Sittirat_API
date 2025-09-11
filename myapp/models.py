from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TouristAttraction(models.Model):
    CATEGORY_CHOICES = [
        ('temple', 'วัด/ศาสนสถาน'),
        ('historical', 'แหล่งโบราณคดี'),
        ('natural', 'แหล่งธรรมชาติ'),
        ('cultural', 'แหล่งวัฒนธรรม'),
        ('market', 'ตลาด/ของฝาก'),
        ('recreation', 'สันทนาการ'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="ชื่อสถานที่")
    description = models.TextField(verbose_name="รายละเอียด")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="หมวดหมู่")
    district = models.CharField(max_length=50, verbose_name="อำเภอ")
    subdistrict = models.CharField(max_length=50, verbose_name="ตำบล")
    address = models.TextField(verbose_name="ที่อยู่")
    latitude = models.FloatField(null=True, blank=True, verbose_name="ละติจูด")
    longitude = models.FloatField(null=True, blank=True, verbose_name="ลองจิจูด")
    opening_hours = models.CharField(max_length=100, blank=True, verbose_name="เวลาเปิด-ปิด")
    entrance_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="ค่าเข้าชม")
    phone = models.CharField(max_length=15, blank=True, verbose_name="เบอร์โทร")
    website = models.URLField(blank=True, verbose_name="เว็บไซต์")
    is_active = models.BooleanField(default=True, verbose_name="เปิดให้เข้าชม")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="คะแนน")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "สถานที่ท่องเที่ยว"
        verbose_name_plural = "สถานที่ท่องเที่ยว"
        ordering = ['-rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.district})"

class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'โรงแรม'),
        ('resort', 'รีสอร์ท'),
        ('guesthouse', 'เกสต์เฮาส์'),
        ('homestay', 'โฮมสเตย์'),
        ('hostel', 'หอสเตล'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="ชื่อที่พัก")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="ประเภท")
    description = models.TextField(verbose_name="รายละเอียด")
    district = models.CharField(max_length=50, verbose_name="อำเภอ")
    address = models.TextField(verbose_name="ที่อยู่")
    phone = models.CharField(max_length=15, verbose_name="เบอร์โทร")
    email = models.EmailField(blank=True, verbose_name="อีเมล")
    website = models.URLField(blank=True, verbose_name="เว็บไซต์")
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="ราคาต่อคืน (เริ่มต้น)")
    total_rooms = models.IntegerField(verbose_name="จำนวนห้องทั้งหมด")
    available_rooms = models.IntegerField(verbose_name="ห้องว่าง")
    amenities = models.TextField(blank=True, verbose_name="สิ่งอำนวยความสะดวก")
    check_in_time = models.TimeField(verbose_name="เวลาเช็คอิน")
    check_out_time = models.TimeField(verbose_name="เวลาเช็คเอาท์")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="คะแนน")
    is_active = models.BooleanField(default=True, verbose_name="เปิดให้บริการ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_type_display(self) -> str:
        # ให้ static checker รู้จัก และ fallback ใช้ค่า label จาก TYPE_CHOICES
        return dict(self.TYPE_CHOICES).get(self.type, self.type)

class TourPackage(models.Model):
    DURATION_CHOICES = [
        ('half_day', 'ครึ่งวัน'),
        ('full_day', '1 วัน'),
        ('2_days', '2 วัน 1 คืน'),
        ('3_days', '3 วัน 2 คืน'),
        ('custom', 'กำหนดเอง'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="ชื่อแพ็คเกจ")
    description = models.TextField(verbose_name="รายละเอียด")
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, verbose_name="ระยะเวลา")
    price_adult = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="ราคาผู้ใหญ่")
    price_child = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="ราคาเด็ก")
    max_participants = models.IntegerField(verbose_name="จำนวนผู้เข้าร่วมสูงสุด")
    included_services = models.TextField(verbose_name="บริการที่รวม")
    excluded_services = models.TextField(blank=True, verbose_name="บริการที่ไม่รวม")
    meeting_point = models.CharField(max_length=200, verbose_name="จุดนัดพบ")
    is_active = models.BooleanField(default=True, verbose_name="เปิดให้บริการ")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="คะแนน")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ความสัมพันธ์กับสถานที่ท่องเที่ยว
    attractions = models.ManyToManyField(TouristAttraction, blank=True, verbose_name="สถานที่ในแพ็คเกจ")

    class Meta:
        verbose_name = "แพ็คเกจทัวร์"
        verbose_name_plural = "แพ็คเกจทัวร์"
        ordering = ['-rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_duration_display()})"

class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, verbose_name="เบอร์โทร")
    id_card = models.CharField(max_length=13, blank=True, verbose_name="เลขบัตรประชาชน")
    address = models.TextField(verbose_name="ที่อยู่")
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name="ผู้ติดต่อฉุกเฉิน")
    emergency_phone = models.CharField(max_length=15, blank=True, verbose_name="เบอร์ติดต่อฉุกเฉิน")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "นักท่องเที่ยว"
        verbose_name_plural = "นักท่องเที่ยว"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('accommodation', 'จองที่พัก'),
        ('tour_package', 'จองแพ็คเกจทัวร์'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'รอการยืนยัน'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('paid', 'ชำระเงินแล้ว'),
        ('completed', 'เสร็จสิ้น'),
        ('cancelled', 'ยกเลิก'),
    ]
    
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES, verbose_name="ประเภทการจอง")
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name="นักท่องเที่ยว")
    
    # สำหรับจองที่พัก
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ที่พัก")
    check_in_date = models.DateField(null=True, blank=True, verbose_name="วันเช็คอิน")
    check_out_date = models.DateField(null=True, blank=True, verbose_name="วันเช็คเอาท์")
    rooms = models.IntegerField(null=True, blank=True, verbose_name="จำนวนห้อง")
    
    # สำหรับจองทัวร์
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="แพ็คเกจทัวร์")
    tour_date = models.DateField(null=True, blank=True, verbose_name="วันทัวร์")
    adults = models.IntegerField(null=True, blank=True, verbose_name="จำนวนผู้ใหญ่")
    children = models.IntegerField(default=0, verbose_name="จำนวนเด็ก")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ยอดรวม")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")
    special_requests = models.TextField(blank=True, verbose_name="ความต้องการพิเศษ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "การจอง"
        verbose_name_plural = "การจอง"
        ordering = ['-created_at']

    def __str__(self):
        if self.booking_type == 'accommodation':
            return f"จองที่พัก: {self.accommodation.name} - {self.tourist.user.username}"
        else:
            return f"จองทัวร์: {self.tour_package.name} - {self.tourist.user.username}"

class Review(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name="นักท่องเที่ยว")
    attraction = models.ForeignKey(TouristAttraction, on_delete=models.CASCADE, null=True, blank=True, verbose_name="สถานที่ท่องเที่ยว")
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True, blank=True, verbose_name="ที่พัก")
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="แพ็คเกจทัวร์")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="คะแนน")
    comment = models.TextField(verbose_name="ความคิดเห็น")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "รีวิว"
        verbose_name_plural = "รีวิว"
        ordering = ['-created_at']
    def __str__(self):
        # แสดงเป้าหมายของรีวิว (สถานที่ / ที่พัก / แพ็คเกจ)
        target = self.attraction or self.accommodation or self.tour_package
        return f"รีวิว: {target} - {self.rating}/5"