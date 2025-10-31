from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/application_list.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def get_queryset(self):
        # Show applications for jobs created by this employer
        return Application.objects.filter(
            job__created_by=self.request.user
        ).order_by('-applied_date')


class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/my_applications.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def get_queryset(self):
        # Show applications submitted by the current user (job seeker)
        return Application.objects.filter(
            applicant=self.request.user
        ).order_by('-applied_date')


class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.created_by




class ApplicationStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    form_class = ApplicationStatusForm
    template_name = 'applications/application_status_update.html'
    success_url = reverse_lazy('applications:application_list')
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.created_by
    
    def form_valid(self, form):
        old_status = self.object.status
        response = super().form_valid(form)
        
        # Send email notification if status changed
        if old_status != self.object.status:
            self.send_status_notification(old_status, self.object.status)
            messages.success(self.request, f'Application status updated to {self.object.get_status_display()}')
        
        return response
    
    def send_status_notification(self, old_status, new_status):
        application = self.object
        subject = f'Application Status Update - {application.job.title}'
        
        # Get the old status display name
        old_status_display = dict(Application.STATUS_CHOICES).get(old_status, old_status)
        new_status_display = dict(Application.STATUS_CHOICES).get(new_status, new_status)
        
        message = f"""
        Hello {application.applicant.get_full_name()},
        
        Your application for the position "{application.job.title}" at {application.job.company.name} 
        has been updated from "{old_status_display}" to "{new_status_display}".
        
        Job Details:
        - Position: {application.job.title}
        - Company: {application.job.company.name}
        - Location: {application.job.location}
        
        Thank you for your interest in this position.
        
        Best regards,
        {application.job.company.name} Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [application.applicant.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't break the flow
            print(f"Failed to send email: {e}")

