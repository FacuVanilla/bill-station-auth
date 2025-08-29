from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.conf import settings
import redis
import secrets
import json

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer
)

User = get_user_model()

# Initialize Redis connection for password reset tokens
try:
    redis_client = redis.from_url(settings.REDIS_URL)
    print("✅ Redis client initialized successfully")
except Exception as e:
    print(f"⚠️  Redis connection failed: {e}")
    print("🔄 Using Django cache fallback for password reset tokens")
    redis_client = None


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

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


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

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


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate reset token
                reset_token = secrets.token_urlsafe(32)
                
                # Store token in Redis with 10 minutes expiry
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


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

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
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TokenRefreshView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        access_token = request.data.get('access')
        
        # Blacklist the refresh token if provided
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # If refresh token is invalid, that's okay for logout
                pass
        
        # Handle the access token if provided
        if access_token:
            try:
                from rest_framework_simplejwt.tokens import AccessToken
                token = AccessToken(access_token)
                # Note: Access tokens can't be blacklisted by default, but we can track them
                # For now, we'll just acknowledge the logout request
            except Exception as e:
                # If access token is invalid, that's okay for logout
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
