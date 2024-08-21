from os import link
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


from django.core.files.storage import FileSystemStorage

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user_type = serializer.validated_data['user_type']
            print(user_type)
            
            # Handle the file upload separately
            profile_photo = serializer.validated_data.get('profile_photo')
            filename = None
            if profile_photo:
                fs = FileSystemStorage()
                filename = fs.save(profile_photo.name, profile_photo)
                file_url = fs.url(filename)

            # Store other data in the session (excluding the file)
            user_data = serializer.validated_data.copy()
            user_data.pop('profile_photo', None)  # Remove profile photo from session data

            otp = random.randint(100000, 999999)
            request.session['user_data'] = user_data
            request.session['otp'] = otp
            request.session['profile_photo_path'] = filename  # Store the file path

            # Send OTP to email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp}.",
                from_email="your_email@example.com",
                recipient_list=[email],
            )

            return Response({"message": "OTP sent to your email. Please verify to complete registration."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def post(self, request):
        otp = request.data.get('otp')
        session_otp = request.session.get('otp')
        user_data = request.session.get('user_data')
        profile_photo_path = request.session.get('profile_photo_path')

        if otp and session_otp and otp == str(session_otp):
            # OTP is correct, create or verify user
            user = CustomUser.objects.create(
                email=user_data['email'],
                user_type=user_data['user_type'],
                phone=user_data.get('phone'),
                occupation=user_data.get('occupation', '')
            )
            user.set_password(user_data['password'])
            user.save()

            # Link the uploaded file to the user profile
            if profile_photo_path:
                fs = FileSystemStorage()
                user.profile_photo = fs.url(profile_photo_path)
                user.save()
            if user_data['user_type'] == 'landlord':
                landlord = Landlord.objects.get(user=user.id)
                landlord.unique_code = landlord.generate_unique_code()

                landlord.save()
                send_mail(
                    subject="Your Unique Code",
                    message=f"Your Unique code is {landlord.unique_code}.",
                    from_email="jayanthunofficial@gmail.com",
                    recipient_list=[user.email]
                )

            # Clear session data
            del request.session['otp']
            del request.session['user_data']
            del request.session['profile_photo_path']

            # Generate tokens
            token_data = get_tokens_for_user(user)
            return Response(token_data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


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

