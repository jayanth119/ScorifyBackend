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
from core.models import Tenant, User
from .serializers import TenantProfileSetupSerializer
import random
from core.models import Tenant, Agent, Landlord
from .serializers import TenantProfileSetupSerializer, AgentProfileSetupSerializer, LandlordProfileSetupSerializer
from django.core.files.storage import FileSystemStorage
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.crypto import get_random_string
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from datetime import timedelta
from django.contrib.auth import authenticate, get_user_model

# Get the user model
User = get_user_model()

# Function to generate tokens upon user login
def generate_tokens_for_user(user):
    """
    Generates a new access and refresh token for a given user.

    Args:
        user (User): The user object for whom the tokens are being generated.

    Returns:
        dict: A dictionary containing the new access and refresh tokens.
    """
    # Create a new refresh token for the user
    refresh = RefreshToken.for_user(user)
    
    # Adding custom claims to the access token
    access_token = refresh.access_token
    access_token['user_id'] = str(user.id)  # Convert UUID to string
    
    # Set custom expiration if needed (Optional)
    access_token.set_exp(lifetime=timedelta(minutes=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']))
    
    return {
        'access': str(access_token),
        'refresh': str(refresh)
    }

# Function to refresh tokens when a valid refresh token is provided
def refresh_tokens(refresh_token):
    """
    Refreshes the access and refresh tokens using a provided refresh token.

    Args:
        refresh_token (str): The refresh token used to generate new tokens.

    Returns:
        dict: A dictionary containing the new access and refresh tokens.
    """
    try:
        # Attempt to create a new RefreshToken instance
        old_refresh = RefreshToken(refresh_token)
        
        # Extract the user ID from the token and convert to string
        user_id = old_refresh['user_id']
        
        # Retrieve the user instance based on the user ID
        user = User.objects.get(id=user_id)
        
        # Generate a new refresh token for the user
        new_refresh = RefreshToken.for_user(user)
        
        # Adding custom claims to the new access token
        new_access_token = new_refresh.access_token
        new_access_token['user_id'] = str(user.id)  # Convert UUID to string
        
        return {
            'access': str(new_access_token),
            'refresh': str(new_refresh)
        }

    except (TokenError, InvalidToken):
        # If the token is invalid or expired, raise an appropriate error
        raise InvalidToken("Invalid or expired refresh token.")
    except User.DoesNotExist:
        # If the user is not found in the database, raise an appropriate error
        raise InvalidToken("User not found for the provided token.")

# APIView to handle user login and generate tokens
class CustomLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view for login

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user using Django's built-in authentication
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # If authentication is successful, generate tokens for the user
            tokens = generate_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            # If authentication fails, return an error response
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

# APIView to handle token refresh requests
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Refresh the tokens using the provided refresh token
            tokens = refresh_tokens(refresh_token)
            return Response(tokens, status=status.HTTP_200_OK)
        
        except InvalidToken as e:
            # If the refresh token is invalid or expired, return an error response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class CustomTokenRefreshView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Get the refresh token from the request data
#         refresh_token = request.data.get('refresh')
#         if refresh_token is None:
#             return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             # Attempt to create a new RefreshToken instance
#             old_refresh = RefreshToken(refresh_token)
            
#             # Get the user from the old refresh token
#             user = old_refresh.user
            
#             # Generate a new refresh token for the user
#             new_refresh = RefreshToken.for_user(user)
            
#             # Prepare the response with the new access and refresh tokens
#             data = {
#                 'access': str(new_refresh.access_token),  # New access token
#                 'refresh': str(new_refresh)  # New refresh token
#             }
#             return Response(data, status=status.HTTP_200_OK)
        
#         except (TokenError, InvalidToken):
#             # Handle invalid or expired refresh tokens
#             return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
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
                link = f"scorify:///change-pass/{user.id}/"
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
    



# class TenantProfileSetupView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         if user.user_type != 'tenant':
#             return Response({"error": "Only tenants can set up a profile."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = TenantProfileSetupSerializer(data=request.data)
#         if serializer.is_valid():
#             tenant = Tenant.objects.get(user=user)
#             tenant.name = serializer.validated_data['name']
#             tenant.phone = serializer.validated_data['phone']
#             tenant.occupation = serializer.validated_data['occupation']
#             tenant.save()

#             return Response({"message": "Profile setup successful."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            if user_data['user_type'] == "tenant":
                unique_code = request.session.get('unique_code')
                landlord  = Landlord.objects.get(unique_code=unique_code)
                tenant = Tenant.objects.create(
                    user=user,
                    name=user_data['email'],
                    landlord = landlord,
                    phone= user_data.get('phone'),
                )
                tenant.save()

            # Clear session data
            del request.session['otp']
            del request.session['user_data']
            del request.session['profile_photo_path']

            # Generate tokens
            token_data = get_tokens_for_user(user)
            return Response(token_data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    

class TenantRegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            unique_code = user_data.get('code')

            try:
                landlord = Landlord.objects.get(unique_code=unique_code)
            except Landlord.DoesNotExist:
                return Response({"error": "Invalid unique code."}, status=status.HTTP_404_NOT_FOUND)

            # Handle profile photo separately
            profile_photo = user_data.pop('profile_photo', None)

            # Generate OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')

            # Create the user
            user = CustomUser.objects.create(
                email=user_data['email'],
                user_type=user_data['user_type'],
                occupation=user_data.get('occupation', ''),
                phone=user_data.get('phone', ''),
            )
            user.set_password(user_data['password'])
            user.save()

            # Create the tenant profile
            tenant = Tenant.objects.create(
                user=user,
                name=user_data.get('name'),
                email=user_data['email'],
                otp=otp,
                profile_photo=profile_photo,
                landlord=landlord  # Link the tenant to the landlord
            )

            # Send OTP email
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp}.",
                from_email="jayanthunoffical@gmail.com",
                recipient_list=[user_data['email']],
            )

            return Response({"message": "OTP sent to your email. Please verify to complete registration."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TenantOTPVerificationView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required for verification."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tenant = Tenant.objects.get(email=email)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant profile does not exist for the given email."}, status=status.HTTP_404_NOT_FOUND)

        if tenant.otp == otp:
            tenant.is_verified = True
            tenant.otp = None  # Clear OTP after successful verification
            tenant.save()
            token_data = get_tokens_for_user(tenant.user)
            return Response(token_data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


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

