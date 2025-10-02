"""
Simple API for Vercel deployment - No database required
"""
import json
import os
from datetime import datetime

def application(environ, start_response):
    # Get request path
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # CORS headers
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type'),
    ]
    
    # Handle OPTIONS request for CORS
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']
    
    # API Routes
    if path == '/' or path == '/api/':
        response = {
            "message": "Welcome to Sittirat Tourism API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "/api/": "API Information",
                "/api/tourist-attractions/": "Tourist Attractions List",
                "/api/accommodations/": "Accommodations List", 
                "/api/tour-packages/": "Tour Packages List",
                "/api/health/": "Health Check"
            }
        }
        
    elif path == '/api/tourist-attractions/' or path == '/api/tourist-attractions':
        response = {
            "count": 3,
            "results": [
                {
                    "id": 1,
                    "name": "วัดพระแก้ว",
                    "description": "วัดพระแก้วเป็นวัดที่สำคัญที่สุดในประเทศไทย",
                    "location": "กรุงเทพมหานคร",
                    "category": "วัด",
                    "opening_hours": "08:30-15:30",
                    "entrance_fee": 500.00
                },
                {
                    "id": 2,
                    "name": "เขาใหญ่",
                    "description": "อุทยานแห่งชาติเขาใหญ่",
                    "location": "นครราชสีมา",
                    "category": "ธรรมชาติ",
                    "opening_hours": "06:00-18:00",
                    "entrance_fee": 40.00
                },
                {
                    "id": 3,
                    "name": "หาดป่าตอง",
                    "description": "หาดทรายขาวที่สวยงามในภูเก็ต",
                    "location": "ภูเก็ต",
                    "category": "ชายหาด",
                    "opening_hours": "24 ชั่วโมง",
                    "entrance_fee": 0.00
                }
            ]
        }
        
    elif path == '/api/accommodations/' or path == '/api/accommodations':
        response = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "name": "โรงแรมแกรนด์ พาเลซ",
                    "description": "โรงแรมหรูใจกลางกรุงเทพฯ",
                    "location": "กรุงเทพมหานคร", 
                    "accommodation_type": "โรงแรม",
                    "price_per_night": 3500.00,
                    "rating": 4.5
                },
                {
                    "id": 2,
                    "name": "รีสอร์ทชายหาด ภูเก็ต",
                    "description": "รีสอร์ทริมทะเลสวยงาม",
                    "location": "ภูเก็ต",
                    "accommodation_type": "รีสอร์ท", 
                    "price_per_night": 2800.00,
                    "rating": 4.2
                }
            ]
        }
        
    elif path == '/api/tour-packages/' or path == '/api/tour-packages':
        response = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "name": "ทัวร์เชียงใหม่ 3 วัน 2 คืน",
                    "description": "เที่ยวเชียงใหม่แบบครบครัน",
                    "duration": 3,
                    "price": 8500.00,
                    "max_participants": 25
                },
                {
                    "id": 2,
                    "name": "ทัวร์ภูเก็ต 4 วัน 3 คืน",
                    "description": "สนุกกับทะเลอันดามัน",
                    "duration": 4,
                    "price": 12500.00,
                    "max_participants": 30
                }
            ]
        }
        
    elif path == '/api/health/' or path == '/api/health':
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "server": "Vercel Serverless",
            "api_version": "1.0.0"
        }
        
    else:
        start_response('404 Not Found', headers)
        response = {
            "error": "Not Found",
            "message": f"Endpoint {path} not found",
            "available_endpoints": ["/api/", "/api/tourist-attractions/", "/api/accommodations/", "/api/tour-packages/", "/api/health/"]
        }
        return [json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8')]
    
    # Return successful response
    start_response('200 OK', headers)
    return [json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8')]

# For Vercel
app = application
handler = application