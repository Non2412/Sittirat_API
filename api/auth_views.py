from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Tourist
from .serializers import UserSerializer, TouristSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """สมัครสมาชิกใหม่"""
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        phone = request.data.get('phone', '')
        address = request.data.get('address', '')
        
        # ตรวจสอบข้อมูลที่จำเป็น
        if not all([username, email, password]):
            return Response(
                {'error': 'กรุณากรอกข้อมูล username, email และ password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ตรวจสอบว่า username หรือ email มีอยู่แล้วหรือไม่
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username นี้มีอยู่แล้ว'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email นี้มีอยู่แล้ว'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # สร้าง User ใหม่
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # สร้าง Tourist profile
        tourist = Tourist.objects.create(
            user=user,
            phone=phone,
            address=address
        )
        
        # ส่งข้อมูลกลับ
        user_serializer = UserSerializer(user)
        tourist_serializer = TouristSerializer(tourist)
        
        return Response({
            'message': 'สมัครสมาชิกสำเร็จ',
            'user': user_serializer.data,
            'tourist': tourist_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError as e:
        return Response(
            {'error': 'เกิดข้อผิดพลาดในการสร้างบัญชี'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """เข้าสู่ระบบ"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'กรุณากรอก username และ password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ตรวจสอบการเข้าสู่ระบบ
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # ดึงข้อมูล Tourist ถ้ามี
                try:
                    tourist = Tourist.objects.get(user=user)
                    tourist_data = TouristSerializer(tourist).data
                except Tourist.DoesNotExist:
                    tourist_data = None
                
                return Response({
                    'message': 'เข้าสู่ระบบสำเร็จ',
                    'user': UserSerializer(user).data,
                    'tourist': tourist_data
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'บัญชีผู้ใช้ถูกระงับ'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {'error': 'Username หรือ Password ไม่ถูกต้อง'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def logout_view(request):
    """ออกจากระบบ"""
    try:
        from django.contrib.auth import logout
        logout(request)
        return Response(
            {'message': 'ออกจากระบบสำเร็จ'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def profile_view(request):
    """ดูข้อมูลโปรไฟล์"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'กรุณาเข้าสู่ระบบ'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        tourist = Tourist.objects.get(user=request.user)
        return Response({
            'user': UserSerializer(request.user).data,
            'tourist': TouristSerializer(tourist).data
        })
    except Tourist.DoesNotExist:
        return Response({
            'user': UserSerializer(request.user).data,
            'tourist': None
        })