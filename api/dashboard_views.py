from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from companies.models import Company
from jobs.models import Job
from applications.models import Application
from .serializers import ApplicationSerializer, JobSerializer


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics (employer only)"""
        if not request.user.profile.is_employer:
            return Response(
                {'error': 'This endpoint is for employers only'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            company = request.user.company
        except Company.DoesNotExist:
            return Response(
                {'error': 'No company profile found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_jobs = Job.objects.filter(created_by=request.user).count()
        active_jobs = Job.objects.filter(created_by=request.user, is_active=True).count()
        total_applications = Application.objects.filter(job__created_by=request.user).count()
        pending_applications = Application.objects.filter(
            job__created_by=request.user, 
            status='applied'
        ).count()
        
        recent_applications = Application.objects.filter(
            job__created_by=request.user
        ).order_by('-applied_date')[:10]
        
        recent_jobs = Job.objects.filter(
            created_by=request.user
        ).order_by('-posted_date')[:5]
        
        data = {
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'recent_applications': ApplicationSerializer(recent_applications, many=True).data,
            'recent_jobs': JobSerializer(recent_jobs, many=True).data,
        }
        
        return Response(data)


