from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'phone', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("รหัสผ่านไม่ตรงกัน")
        return attrs

    def create(self, validated_data):
        # ลบ password_confirm ออก
        validated_data.pop('password_confirm', None)
        
        # แยกข้อมูล Tourist ออก
        phone = validated_data.pop('phone', '')
        address = validated_data.pop('address', '')
        
        # สร้าง User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Import Tourist ภายในฟังก์ชันเพื่อหลีกเลี่ยง circular import
        from .models import Tourist
        
        # สร้าง Tourist profile
        Tourist.objects.create(
            user=user,
            phone=phone,
            address=address
        )
        
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()