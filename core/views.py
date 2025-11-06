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
        user = self.request.user
        
        if user.is_authenticated:
            # Check if the user has a profile, which might not be the case for superusers
            # or if the post-save signal failed.
            if hasattr(user, 'profile'):
                context['user_type'] = user.profile.user_type
                
                if user.profile.user_type == 'employer':
                    # --- Employer Dashboard Data ---
                    employer_jobs = Job.objects.filter(created_by=user)
                    context['recent_jobs'] = employer_jobs.order_by('-posted_date')[:6]
                    context['total_jobs'] = employer_jobs.count()
                    
                    applications = Application.objects.filter(job__in=employer_jobs)
                    context['total_applications'] = applications.count()
                    context['pending_applications'] = applications.filter(status='applied').count()
                    
                    # Application status breakdown
                    status_counts = applications.values('status').annotate(count=Count('status'))
                    status_map = {item['status']: item['count'] for item in status_counts}
                    
                    context['under_review'] = status_map.get('under_review', 0)
                    context['interviews'] = status_map.get('interview', 0)
                    context['offers'] = status_map.get('offer', 0)
                    context['rejected'] = status_map.get('rejected', 0)

                elif user.profile.user_type == 'job_seeker':
                    # --- Seeker Dashboard Data ---
                    my_applications = Application.objects.filter(applicant=user).order_by('-applied_date')
                    context['recent_applications'] = my_applications[:5]
                    context['total_applications_submitted'] = my_applications.count()

                    # Application status breakdown
                    status_counts = my_applications.values('status').annotate(count=Count('status'))
                    status_map = {item['status']: item['count'] for item in status_counts}

                    context['applied_count'] = status_map.get('applied', 0)
                    context['under_review_count'] = status_map.get('under_review', 0)
                    context['interview_count'] = status_map.get('interview', 0)
                    context['offer_count'] = status_map.get('offer', 0)

                    # Suggested jobs (exclude jobs already applied to)
                    applied_job_ids = my_applications.values_list('job_id', flat=True)
                    context['suggested_jobs'] = Job.objects.filter(is_active=True).exclude(id__in=applied_job_ids).order_by('-posted_date')[:5]
            else:
                # Default context for authenticated users without a profile (e.g., admin)
                context['user_type'] = 'admin' # or some other default
                context['recent_jobs'] = Job.objects.filter(is_active=True).order_by('-posted_date')[:4]

        else:
            # --- Unauthenticated User Homepage Data ---
            context['recent_jobs'] = Job.objects.filter(is_active=True).order_by('-posted_date')[:4]
        
        return context