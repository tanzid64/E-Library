from typing import Any
from django.shortcuts import render
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from .constants import send_registration_email
# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts.html'
    success_url = reverse_lazy('registration')
    form_class = UserRegistrationForm
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Account Creation Successfull')
        login(self.request, user)
        send_registration_email(user,'Account Registration','registration_mail.html')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Create An Account',
            'type': '1',
        })
        return context
    
class UserLoginView(LoginView):
    template_name = 'accounts.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Log In Your Account',
            'type': '2',
        })
        return context
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')
    
class UserProfileView(DetailView):
    template_name = 'profile.html'
    def get_object(self):
        return self.request.user
    
class UserProfileUpdateView(UpdateView):
    template_name = 'accounts.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('profile')
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile Updated Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.danger(self.request, 'Information Incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Update Your Profile',
            'type': '3',
        })
        return context
    
class UserPasswordUpdateView(PasswordChangeView):
    template_name = 'accounts.html'
    success_url = reverse_lazy('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Update Your Password',
            'type': '4',
        })
        return context