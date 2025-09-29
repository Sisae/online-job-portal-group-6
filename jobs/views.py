from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from companies.models import Company
from .models import Job
from .forms import JobForm


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 12
    
    def get_queryset(self):
        # Only show jobs created by the current user
        return Job.objects.filter(created_by=self.request.user).order_by('-posted_date')


class JobDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.created_by


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:job_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            form.instance.company = self.request.user.company
        except Company.DoesNotExist:
            messages.error(self.request, 'You must create a company profile before posting jobs.')
            return redirect('companies:my_company')
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)


class JobEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:job_list')
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
    success_url = reverse_lazy('jobs:job_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        job = self.get_object()
        return self.request.user == job.created_by

