from django import forms
from .models import Book, Category

class AddBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['name', 'language', 'quantity', 'price', 'category', 'description', 'image']
        widgets = {
            'category' : forms.CheckboxSelectMultiple
        }