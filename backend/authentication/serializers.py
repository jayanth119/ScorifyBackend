from rest_framework import serializers
from .models import CustomUser  
from core.models import Tenant
from django.contrib.auth import authenticate

from core.models import Tenant, Agent, Landlord

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile_photo = serializers.ImageField(required=False)
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    occupation = serializers.CharField(max_length=255, required=False)
    code = serializers.CharField(write_only=True, required=False)  # Add OTP field for tenants

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'user_type', 'profile_photo', 'name', 'phone', 'occupation', 'code']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        
        if CustomUser.objects.filter(email=attrs['email']).exists():
            user = CustomUser.objects.get(email=attrs['email'])
            if not user.is_verified:
                raise serializers.ValidationError({"email": "Account with this email already exists and is not verified. Please verify the account."})
            else:
                raise serializers.ValidationError({"email": "Email already exists."})

        # OTP validation for tenants
        if attrs['user_type'] == 'tenant':
            code = attrs.get('code')
            if not code:
                raise serializers.ValidationError({"Code": "Code is required for tenant registration."})
            
            # Check if the OTP matches any landlord's unique code
            if not Landlord.objects.filter(unique_code=code).exists():
                raise serializers.ValidationError({"code": "Invalid CODE. No landlord with this code."})

        return attrs
    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            phone=validated_data['phone'],
            occupation=validated_data.get('occupation', ''),
            profile_photo=validated_data.get('profile_photo', None)
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email is required for login.")
        if password is None:
            raise serializers.ValidationError("Password is required for login.")
        return attrs
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True)
    password1 = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")
        if password != password1:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

class TenantProfileSetupSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = Tenant
        fields = ['name', 'email', 'occupation', 'profile_photo']

class TenantOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class AgentProfileSetupSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = Agent
        fields = ['name', 'phone', 'profile_photo']

class LandlordProfileSetupSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = Landlord
        fields = ['name', 'phone', 'profile_photo']
