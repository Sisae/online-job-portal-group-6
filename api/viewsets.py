from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import UserProfile
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from .serializers import (
    UserSerializer, UserProfileSerializer, CompanySerializer, 
    JobSerializer, JobCreateSerializer, ApplicationSerializer, 
    ApplicationCreateSerializer, ApplicationStatusUpdateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            if hasattr(self.request.user, 'company'):
                return Company.objects.filter(owner=self.request.user)
            return Company.objects.none()
        return Company.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_company(self, request):
        try:
            company = request.user.company
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response(
                {'error': 'No company profile found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return JobCreateSerializer
        return JobSerializer
    
    def get_queryset(self):
        if self.request.user.profile.is_employer:
            return Job.objects.filter(created_by=self.request.user)
        else:
            return Job.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'company'):
            serializer.save(company=self.request.user.company, created_by=self.request.user)
        else:
            raise serializers.ValidationError("User must have a company profile to create jobs")
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        queryset = Job.objects.filter(is_active=True)
        
        search = request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__name__icontains=search) |
                Q(location__icontains=search)
            )
        
        job_type = request.query_params.get('job_type', None)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        
        location = request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        remote = request.query_params.get('remote', None)
        if remote is not None:
            queryset = queryset.filter(remote=remote.lower() == 'true')
        
        queryset = queryset.order_by('-posted_date')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ApplicationStatusUpdateSerializer
        return ApplicationSerializer
    
    def get_queryset(self):
        if self.request.user.profile.is_employer:
            return Application.objects.filter(job__created_by=self.request.user)
        else:
            return Application.objects.filter(applicant=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        if not request.user.profile.is_employer or application.job.created_by != request.user:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            old_status = application.status
            serializer.save()
            
            if old_status != application.status:
                from applications.views import ApplicationStatusUpdateView
                view = ApplicationStatusUpdateView()
                view.object = application
                view.send_status_notification(old_status, application.status)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


