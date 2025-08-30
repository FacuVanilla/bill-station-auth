from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import redis
import secrets
import json
import os

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    TokenRefreshSerializer,
    LogoutSerializer
)

User = get_user_model()

# Initialize Redis connection for password reset tokens
redis_client = None
try:
    redis_url = os.environ.get('REDIS_URL')
    if redis_url:
        redis_client = redis.from_url(redis_url)
        print("✅ Redis client initialized successfully")
    else:
        print("⚠️  No REDIS_URL found, using Django cache fallback")
except Exception as e:
    print(f"⚠️  Redis connection failed: {e}")
    print("🔄 Using Django cache fallback for password reset tokens")


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    """
    Register a new user account
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user account",
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe",
                            "date_joined": "2025-01-01T00:00:00Z",
                            "last_login": None
                        },
                        "tokens": {
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        }
                    }
                }
            ),
            400: "Bad request - validation errors"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(generics.GenericAPIView):
    """
    Authenticate and login a user
    """
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Authenticate and login a user",
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe",
                            "date_joined": "2025-01-01T00:00:00Z",
                            "last_login": "2025-01-01T12:00:00Z"
                        },
                        "tokens": {
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        }
                    }
                }
            ),
            400: "Bad request - invalid credentials"
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(generics.GenericAPIView):
    """
    Request a password reset token
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Request a password reset token",
        responses={
            200: openapi.Response(
                description="Password reset token generated",
                examples={
                    "application/json": {
                        "message": "Password reset token generated successfully",
                        "reset_token": "abc123def456...",
                        "expires_in": "10 minutes",
                        "note": "In production, this token would be sent via email"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate reset token
                reset_token = secrets.token_urlsafe(32)
                
                # Store token in Redis/cache with 10 minutes expiry
                cache_key = f"password_reset_{reset_token}"
                cache_data = {
                    'user_id': user.id,
                    'email': user.email
                }
                
                # Use Redis if available, otherwise fallback to Django cache
                if redis_client:
                    redis_client.setex(cache_key, 600, json.dumps(cache_data))  # 10 minutes
                else:
                    cache.set(cache_key, json.dumps(cache_data), timeout=600)  # 10 minutes
                
                # In a real application, you would send this token via email
                # For demo purposes, we'll return it in the response
                return Response({
                    'message': 'Password reset token generated successfully',
                    'reset_token': reset_token,
                    'expires_in': '10 minutes',
                    'note': 'In production, this token would be sent via email'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                # Don't reveal if user exists or not for security
                return Response({
                    'message': 'If the email exists, a password reset token has been generated'
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Confirm password reset with token
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Confirm password reset with token",
        responses={
            200: openapi.Response(
                description="Password reset successful",
                examples={
                    "application/json": {
                        "message": "Password reset successful"
                    }
                }
            ),
            400: "Bad request - invalid or expired token"
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            # Check if token exists in Redis/cache
            cache_key = f"password_reset_{token}"
            
            if redis_client:
                cached_data = redis_client.get(cache_key)
            else:
                cached_data = cache.get(cache_key)
            
            if not cached_data:
                return Response({
                    'error': 'Invalid or expired reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Parse cached data
                if isinstance(cached_data, bytes):
                    cached_data = cached_data.decode('utf-8')
                user_data = json.loads(cached_data)
                user = User.objects.get(id=user_data['user_id'])
                
                # Update password
                user.set_password(new_password)
                user.save()
                
                # Remove token from Redis/cache
                if redis_client:
                    redis_client.delete(cache_key)
                else:
                    cache.delete(cache_key)
                
                return Response({
                    'message': 'Password reset successful'
                }, status=status.HTTP_200_OK)
                
            except (User.DoesNotExist, json.JSONDecodeError):
                return Response({
                    'error': 'Invalid reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={
            200: UserProfileSerializer,
            401: "Unauthorized"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user profile",
        responses={
            200: UserProfileSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(generics.GenericAPIView):
    """
    Refresh JWT access token
    """
    serializer_class = TokenRefreshSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Refresh JWT access token",
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            ),
            400: "Bad request - invalid refresh token"
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                refresh = RefreshToken(refresh_token)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({
                    'error': 'Invalid refresh token'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Logout user and blacklist refresh token",
    request_body=LogoutSerializer,
    responses={
        200: openapi.Response(
            description="Logout successful",
            examples={
                "application/json": {
                    "message": "Logout successful",
                    "note": "Tokens have been invalidated"
                }
            }
        )
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@csrf_exempt
def logout_view(request):
    """
    Logout endpoint that blacklists refresh tokens
    """
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        try:
            refresh_token = serializer.validated_data.get('refresh')
            
            # Blacklist the refresh token if provided
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception as e:
                    # If refresh token is invalid, that's okay for logout
                    pass
            
            return Response({
                'message': 'Logout successful',
                'note': 'Tokens have been invalidated'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': 'Logout successful',
                'note': 'Some tokens may have been invalid already'
            }, status=status.HTTP_200_OK)
    else:
        # Even if serializer is invalid, we can still logout
        return Response({
            'message': 'Logout successful',
            'note': 'Logout completed despite invalid data'
        }, status=status.HTTP_200_OK)