from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from companies.models import Company
from applications.models import Application
from .models import Job
from .forms import JobForm


from django_filters.views import FilterView
from .models import Job
from .forms import JobForm
from .filters import JobFilter


class JobListView(FilterView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    filterset_class = JobFilter
    paginate_by = 9

    def get_queryset(self):
        return Job.objects.filter(is_active=True).order_by('-posted_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The filter object is already in the context as `filter`
        return context


class MyJobsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Job
    template_name = 'jobs/my_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 9
    
    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.is_employer

    def get_queryset(self):
        # Only show jobs created by the current user (for employers)
        return Job.objects.filter(created_by=self.request.user).order_by('-posted_date')


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        user = self.request.user
        
        is_job_creator = (user == job.created_by)
        context['is_job_creator'] = is_job_creator
        
        has_applied = False
        if user.is_authenticated and hasattr(user, 'profile') and user.profile.is_job_seeker:
            has_applied = Application.objects.filter(job=job, applicant=user).exists()
        
        context['has_applied'] = has_applied
        
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # Handle the case where the job does not exist
            messages.error(request, "Sorry, the job you are looking for does not exist.")
            return redirect('jobs:job_list')

        job = self.object
        user = request.user

        is_job_creator = (user.is_authenticated and user == job.created_by)
        is_job_seeker = user.is_authenticated and hasattr(user, 'profile') and user.profile.is_job_seeker
        
        # Public access for active jobs
        if job.is_active:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

        # If job is not active, only allow creator or admin
        if not is_job_creator and not user.is_superuser:
            messages.error(request, "This job is no longer active.")
            return redirect('jobs:job_list')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:my_jobs')

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.is_employer
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            # Ensure the user has a company profile associated
            form.instance.company = Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            messages.error(self.request, 'You must create a company profile before posting jobs.')
            return redirect('companies:company_create')
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)


class JobEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:my_jobs')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('jobs:my_jobs')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.created_by
    
    def form_valid(self, form):
        messages.success(self.request, 'Job deleted successfully.')
        return super().form_valid(form)