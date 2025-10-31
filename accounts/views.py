from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm, CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:home')
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user.profile


class LogoutView(BaseLogoutView):
    """Custom logout view that maintains security while providing user feedback."""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Add message before logout (user context is still available)
            messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


