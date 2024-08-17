from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer,UserLoginSerializer,ForgotPasswordSerializer,ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import CustomUser
from core.models import Tenant
from .serializers import TenantProfileSetupSerializer
import random
from core.models import Tenant, Agent, Landlord
from .serializers import TenantProfileSetupSerializer, AgentProfileSetupSerializer, LandlordProfileSetupSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_data = get_tokens_for_user(user)
            return Response(token_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request,email=email,password=password)
            if user is None:
                return Response({"message":"Invalid Email or Password"},status=status.HTTP_400_BAD_REQUEST)
            token = get_tokens_for_user(user)
            return Response({
                "message":"Login Success",
                "token":token,
                "email":user.email,
                "isAdmin":user.is_admin
            },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ForgotPasswordView(APIView):
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid(): 
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user :
                link = f"http://127.0.0.1:8000/accounts/change-password/{user.id}/"
                send_mail(
                    subject="Forgot Password",
                    message=f"Click the following to reset your password {link}",
                    from_email="jayanthunofficial@gmail.com",
                    recipient_list=[email]
                )
                return Response({"message":"Please check your email"},status=status.HTTP_200_OK)
            return Response({"message":"User doesnot exists"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
   def put(self,request,id):
       serializer = ChangePasswordSerializer(data=request.data)
       if serializer.is_valid():
           password = serializer.validated_data['password']
           user = CustomUser.objects.get(id=id)
           user.set_password(password)
           user.save()
           return Response({"message":"Successfully updated Password "},status=status.HTTP_200_OK)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)           
    



class TenantProfileSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'tenant':
            return Response({"error": "Only tenants can set up a profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TenantProfileSetupSerializer(data=request.data)
        if serializer.is_valid():
            tenant = Tenant.objects.get(user=user)
            tenant.name = serializer.validated_data['name']
            tenant.phone = serializer.validated_data['phone']
            tenant.occupation = serializer.validated_data['occupation']
            tenant.save()

            return Response({"message": "Profile setup successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'tenant':
            return Response({"error": "Only tenants can receive an OTP."}, status=status.HTTP_403_FORBIDDEN)

        otp = random.randint(100000, 999999)
        user.tenant_profile.otp = otp
        user.tenant_profile.save()

        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {otp}.",
            from_email="jayanthunofficial@gmail.com",
            recipient_list=[user.email]
        )

        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
class VerifyOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'tenant':
            return Response({"error": "Only tenants can verify an OTP."}, status=status.HTTP_403_FORBIDDEN)

        otp = request.data.get("otp")
        if str(user.tenant_profile.otp) == otp:
            user.tenant_profile.is_verified = True
            user.tenant_profile.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)



class TenantProfileSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'tenant':
            return Response({"error": "Only tenants can set up a profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TenantProfileSetupSerializer(data=request.data)
        if serializer.is_valid():
            tenant = Tenant.objects.get(user=user)
            tenant.name = serializer.validated_data['name']
            tenant.phone = serializer.validated_data['phone']
            tenant.occupation = serializer.validated_data['occupation']
            if 'profile_photo' in serializer.validated_data:
                tenant.profile_photo = serializer.validated_data['profile_photo']
            tenant.save()

            return Response({"message": "Profile setup successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentProfileSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'agent':
            return Response({"error": "Only agents can set up a profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AgentProfileSetupSerializer(data=request.data)
        if serializer.is_valid():
            agent = Agent.objects.get(user=user)
            agent.name = serializer.validated_data['name']
            agent.phone = serializer.validated_data['phone']
            if 'profile_photo' in serializer.validated_data:
                agent.profile_photo = serializer.validated_data['profile_photo']
            agent.save()

            return Response({"message": "Profile setup successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LandlordProfileSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.user_type != 'landlord':
            return Response({"error": "Only landlords can set up a profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LandlordProfileSetupSerializer(data=request.data)
        if serializer.is_valid():
            landlord = Landlord.objects.get(user=user)
            landlord.name = serializer.validated_data['name']
            landlord.phone = serializer.validated_data['phone']
            if 'profile_photo' in serializer.validated_data:
                landlord.profile_photo = serializer.validated_data['profile_photo']
            landlord.save()

            return Response({"message": "Profile setup successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

