from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login and get authentication token"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'profile': UserProfileSerializer(user.profile).data
            })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout and delete authentication token"""
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except:
                pass
        return Response({'message': 'Logged out successfully'})
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user"""
        from accounts.forms import CustomUserCreationForm
        
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'profile': UserProfileSerializer(user.profile).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


