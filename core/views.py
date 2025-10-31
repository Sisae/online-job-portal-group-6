from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from jobs.models import Job
from applications.models import Application


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Show employer's own jobs
            context['recent_jobs'] = Job.objects.filter(created_by=self.request.user).order_by('-posted_date')[:6]
            context['total_jobs'] = Job.objects.filter(created_by=self.request.user).count()
            
            # Application statistics
            applications = Application.objects.filter(job__created_by=self.request.user)
            context['total_applications'] = applications.count()
            context['pending_applications'] = applications.filter(status='applied').count()
            context['under_review'] = applications.filter(status='under_review').count()
            context['interviews'] = applications.filter(status='interview').count()
            context['offers'] = applications.filter(status='offer').count()
            context['rejected'] = applications.filter(status='rejected').count()
            
            # Recent applications
            context['recent_applications'] = applications.order_by('-applied_date')[:5]
        else:
            # Show some sample jobs for non-authenticated users
            context['recent_jobs'] = Job.objects.filter(is_active=True).order_by('-posted_date')[:6]
            context['total_jobs'] = Job.objects.filter(is_active=True).count()
        
        return context