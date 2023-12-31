from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from .forms import AddBookForm, CommentForm
from django.contrib import messages
from .models import Book, Comment
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

# Email Sending Function
def send_author_email(user, subject, template):
        message = render_to_string(template,{
            'user': user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
# Create your views here.
class AddBookView(LoginRequiredMixin,CreateView):
    template_name = 'book.html'
    success_url = reverse_lazy('profile')
    form_class = AddBookForm
    
    def form_valid(self, form):
        messages.success(self.request, 'Book Added Successfully')
        form.instance.author = self.request.user.profile
        send_author_email(self.request.user, "Add Book to eBOOK", 'add_book_mail.html')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'name': 'Add A Book',
            'type': '1',
        })
        return context
    
class BookDetailsView(DetailView):
    model = Book
    template_name = 'book_details.html'
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        book = self.get_object()

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.profile = self.request.user.profile
            new_comment.save()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        context['comments'] = book.comments.all()
        context['comment_form'] = CommentForm
        return context