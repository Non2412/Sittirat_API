# Sittirat Tourism API

API สำหรับระบบจัดการการท่องเที่ยวจังหวัดศรีสะเกษ ประเทศไทย

## 📋 คุณสมบัติหลัก

- **สถานที่ท่องเที่ยว** - จัดการข้อมูลสถานที่ท่องเที่ยว วัด แหล่งโบราณคดี และแหล่งธรรมชาติ
- **ที่พัก** - ระบบจองและจัดการโรงแรม รีสอร์ท เกสต์เฮาส์ และโฮมสเตย์
- **แพ็คเกจทัวร์** - สร้างและจัดการแพ็คเกจท่องเที่ยว
- **ระบบจอง** - จองที่พักและแพ็คเกจทัวร์
- **รีวิวและคะแนน** - ระบบรีวิวสถานที่และบริการ
- **Dashboard** - สถิติและรายงานการท่องเที่ยว
- **Authentication** - ระบบลงทะเบียนและเข้าสู่ระบบ

## 🛠️ เทคโนโลยีที่ใช้

- **Django** - Web framework
- **Django REST Framework** - RESTful API
- **Token Authentication** - ระบบยืนยันตัวตน
- **PostgreSQL/SQLite** - ฐานข้อมูล

## 📦 การติดตั้ง

### 1. Clone โปรเจค

```bash
git clone https://github.com/Non2412/Sittirat_API.git
cd Sittirat_API
```

### 2. สร้าง Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
# หรือ
venv\Scripts\activate  # สำหรับ Windows
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่าฐานข้อมูล

```bash
python manage.py migrate
```

### 5. สร้าง Superuser (ถ้าต้องการเข้า Admin)

```bash
python manage.py createsuperuser
```

### 6. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

API จะรันที่ `http://localhost:8000/api/`

## 🔌 API Endpoints

### Authentication

```
POST /api/auth/register/     # ลงทะเบียนผู้ใช้ใหม่
POST /api/auth/login/        # เข้าสู่ระบบ
```

### สถานที่ท่องเที่ยว

```
GET    /api/attractions/              # ดูสถานที่ทั้งหมด
GET    /api/attractions/{id}/         # ดูรายละเอียดสถานที่
GET    /api/attractions/search/       # ค้นหาสถานที่
GET    /api/attractions/categories/   # ดูหมวดหมู่
GET    /api/attractions/districts/    # ดูอำเภอทั้งหมด
GET    /api/attractions/popular/      # สถานที่ยอดนิยม
```

**ตัวอย่างการค้นหา:**
```
GET /api/attractions/search/?q=ปราสาท&category=historical&district=กันทรลักษ์&min_rating=4
```

### ที่พัก

```
GET    /api/accommodations/           # ดูที่พักทั้งหมด
GET    /api/accommodations/{id}/      # ดูรายละเอียดที่พัก
GET    /api/accommodations/search/    # ค้นหาที่พัก
GET    /api/accommodations/types/     # ดูประเภทที่พัก
```

**ตัวอย่างการค้นหา:**
```
GET /api/accommodations/search/?q=โรงแรม&type=hotel&max_price=2000&min_rating=3.5
```

### แพ็คเกจทัวร์

```
GET    /api/tour-packages/            # ดูแพ็คเกจทั้งหมด
GET    /api/tour-packages/{id}/       # ดูรายละเอียดแพ็คเกจ
GET    /api/tour-packages/search/     # ค้นหาแพ็คเกจ
GET    /api/tour-packages/durations/  # ดูระยะเวลาทัวร์
```

### การจอง

```
GET    /api/bookings/                       # ดูการจองทั้งหมด (ต้อง login)
POST   /api/bookings/accommodation/create/  # จองที่พัก
POST   /api/bookings/tour/create/           # จองแพ็คเกจทัวร์
PATCH  /api/bookings/{id}/update_status/    # อัปเดตสถานะการจอง
GET    /api/bookings/by_tourist/            # ดูการจองของนักท่องเที่ยว
```

**ตัวอย่างการจองที่พัก:**
```json
POST /api/bookings/accommodation/create/
{
  "tourist_id": 1,
  "accommodation_id": 5,
  "check_in_date": "2025-10-15",
  "check_out_date": "2025-10-17",
  "rooms": 2,
  "special_requests": "ห้องติดกัน"
}
```

**ตัวอย่างการจองทัวร์:**
```json
POST /api/bookings/tour/create/
{
  "tourist_id": 1,
  "tour_package_id": 3,
  "tour_date": "2025-10-20",
  "adults": 2,
  "children": 1,
  "special_requests": "อาหารเจ"
}
```

### รีวิว

```
GET    /api/reviews/                        # ดูรีวิวทั้งหมด
POST   /api/reviews/                        # สร้างรีวิว
GET    /api/reviews/by_attraction/          # ดูรีวิวของสถานที่
GET    /api/reviews/by_accommodation/       # ดูรีวิวของที่พัก
```

### Dashboard & สถิติ

```
GET /api/dashboard/stats/                    # สถิติภาพรวม
GET /api/dashboard/popular-destinations/     # สถานที่ยอดนิยม
GET /api/dashboard/district-stats/           # สถิติแยกตามอำเภอ
GET /api/dashboard/booking-trends/           # แนวโน้มการจอง
GET /api/dashboard/accommodation-availability/ # ความพร้อมใช้งานที่พัก
GET /api/dashboard/sisaket-highlights/       # ไhighlight ศรีสะเกษ
```

## 🔐 Authentication

API ใช้ Token Authentication สำหรับ endpoints ที่ต้องการการยืนยันตัวตน

### การลงทะเบียน

```json
POST /api/auth/register/
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "password_confirm": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "0812345678",
  "address": "123 ถนนหลัก เมืองศรีสะเกษ"
}
```

**Response:**
```json
{
  "message": "ลงทะเบียนสำเร็จ",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### การใช้งาน Token

เพิ่ม Token ใน Header ของทุก request:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## 📊 โครงสร้างข้อมูล

### TouristAttraction (สถานที่ท่องเที่ยว)
- ชื่อ, คำอธิบาย, หมวดหมู่
- อำเภอ, ตำบล, ที่อยู่
- พิกัด (Latitude/Longitude)
- เวลาเปิด-ปิด, ค่าเข้าชม
- คะแนนรีวิว

### Accommodation (ที่พัก)
- ชื่อ, ประเภท, คำอธิบาย
- ราคาต่อคืน
- จำนวนห้องทั้งหมด/ห้องว่าง
- เวลาเช็คอิน-เช็คเอาท์
- สิ่งอำนวยความสะดวก

### TourPackage (แพ็คเกจทัวร์)
- ชื่อ, คำอธิบาย, ระยะเวลา
- ราคาผู้ใหญ่/เด็ก
- จำนวนผู้เข้าร่วมสูงสุด
- บริการที่รวม/ไม่รวม
- สถานที่ในแพ็คเกจ

### Booking (การจอง)
- ประเภทการจอง (ที่พัก/ทัวร์)
- ข้อมูลนักท่องเที่ยว
- วันที่เข้าพัก/วันทัวร์
- จำนวนห้อง/ผู้เข้าร่วม
- สถานะ (รอยืนยัน/ยืนยันแล้ว/ชำระเงิน/เสร็จสิ้น/ยกเลิก)

## 🗂️ โครงสร้างไฟล์

```
api/
├── models.py              # โมเดลฐานข้อมูล
├── serializers.py         # Serializers สำหรับ API
├── views.py               # Views และ ViewSets
├── urls.py                # URL routing
├── auth_serializers.py    # Authentication serializers
├── auth_views.py          # Authentication views
└── admin.py               # Django Admin configuration
```

## 🌟 คุณสมบัติพิเศษ

- **ค้นหาแบบ Full-text** - ค้นหาในหลายฟิลด์พร้อมกัน
- **กรองข้อมูล** - กรองตามหมวดหมู่, อำเภอ, ราคา, คะแนน
- **สถิติและรายงาน** - Dashboard สำหรับวิเคราะห์ข้อมูล
- **ระบบคะแนนและรีวิว** - ให้คะแนนและรีวิวสถานที่/บริการ
- **การจัดการห้องว่าง** - อัพเดตห้องว่างอัตโนมัติเมื่อมีการจอง

## 📝 หมายเหตุ

- API นี้ออกแบบมาสำหรับจังหวัดศรีสะเกษ ประเทศไทย
- รองรับข้อมูลภาษาไทยและการตรวจสอบเบอร์โทรศัพท์ไทย
- ใช้ Django Admin สำหรับจัดการข้อมูล backend

## 🤝 การมีส่วนร่วม

สามารถ Fork โปรเจคและส่ง Pull Request ได้ตามสะดวก

## 📄 License

โปรเจคนี้เปิดให้ใช้งานเพื่อการศึกษา

---

Made with ❤️ for Sisaket Tourism
