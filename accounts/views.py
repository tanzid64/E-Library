from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import FormView, DetailView, UpdateView, ListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from .constants import send_registration_email
from transactions.models import Transaction
from book.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'accounts.html'
    success_url = reverse_lazy('profile')
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
    
class UserLogoutView(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('login')
    
class UserProfileView(LoginRequiredMixin,ListView):
    template_name = 'profile.html'
    model = Transaction
    def get_queryset(self):
        return super().get_queryset().filter(
            profile=self.request.user.profile
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user
        context['profile'] = self.request.user.profile
        context['book_list'] = Book.objects.filter(author=self.request.user.profile)
        return context
    
class AuthorProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user = self.get_object())
        context['profile'] = profile
        context['book_list'] = Book.objects.filter(author = profile)
        return context
    
class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
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
    
class UserPasswordUpdateView(LoginRequiredMixin,PasswordChangeView):
    template_name = 'accounts.html'
    success_url = reverse_lazy('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Update Your Password',
            'type': '4',
        })
        return context
    