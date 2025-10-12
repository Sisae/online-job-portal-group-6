from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Company
from .forms import CompanyForm
from applications.models import Application


class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'
    paginate_by = 12


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('companies:my_company')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Company profile created successfully!')
        return super().form_valid(form)


class CompanyEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/company_form.html'
    success_url = reverse_lazy('companies:my_company')
    
    def test_func(self):
        company = self.get_object()
        return self.request.user == company.owner
    
    def form_valid(self, form):
        messages.success(self.request, 'Company profile updated successfully!')
        return super().form_valid(form)


class MyCompanyView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/my_company.html'
    context_object_name = 'company'
    
    def get_object(self):
        try:
            return Company.objects.get(owner=self.request.user)
        except Company.DoesNotExist:
            return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.object
        if not company:
            context['no_company'] = True
        else:
            jobs = company.jobs.all()
            context['jobs'] = jobs
            context['total_jobs_count'] = jobs.count()
            context['active_jobs_count'] = jobs.filter(is_active=True).count()
            context['total_applications_count'] = Application.objects.filter(job__company=company).count()
        return context