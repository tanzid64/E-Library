from django import forms
from .models import Book, Category, Comment

class AddBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['name', 'language', 'quantity', 'price', 'category', 'description', 'image']
        widgets = {
            'category' : forms.CheckboxSelectMultiple
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']