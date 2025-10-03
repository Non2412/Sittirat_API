# Sittirat Tourism API - Railway Deployment

Django REST API สำหรับระบบท่องเที่ยวศรีสะเกษ

## Railway Deployment Guide

### 1. เตรียม Railway Project
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init
```

### 2. Environment Variables ที่ต้องตั้งใน Railway
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.railway.app
DATABASE_URL=postgresql://user:password@host:port/database  # Railway จะให้อัตโนมัติ
RAILWAY_ENVIRONMENT=production
```

### 3. Deploy to Railway
```bash
# Deploy current branch
railway up

# หรือ link กับ GitHub repository
railway link [your-repo-url]
```

### 4. Database Setup
Railway จะสร้าง PostgreSQL database ให้อัตโนมัติ และ set `DATABASE_URL` environment variable

### 5. Static Files
Railway จะรัน collectstatic อัตโนมัติตาม Procfile

### 6. API Endpoints
- `GET /` - API information
- `GET /api/` - API root
- `GET /admin/` - Django admin
- `GET /api/accommodations/` - ข้อมูลที่พัก
- `GET /api/tourists/` - ข้อมูลนักท่องเที่ยว

### Local Development
```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน migrations
python manage.py migrate

# สร้าง superuser
python manage.py createsuperuser

# รัน development server
python manage.py runserver
```

### Project Structure
```
Sittirat_API/
├── api/                 # Main API app
├── backend/            # Django settings
├── Procfile           # Railway deployment config
├── railway.json       # Railway configuration
├── requirements.txt   # Python dependencies
├── .env.example      # Environment variables example
└── manage.py         # Django management script
```

### Important Files for Railway:
- `Procfile` - กำหนดคำสั่งรัน web server
- `railway.json` - Railway configuration
- `requirements.txt` - Python dependencies
- `.env.example` - ตัวอย่าง environment variables

### Migration from Vercel:
- ลบ `vercel.json` แล้ว
- เพิ่ม `Procfile` และ `railway.json`
- ปรับ `settings.py` ให้รองรับ Railway
- เพิ่ม environment variables ใน Railway dashboard