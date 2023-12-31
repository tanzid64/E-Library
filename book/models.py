from django.db import models
from core.models import BaseModel
from accounts.models import Profile
# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    def __str__(self) -> str:
        return self.name

class Book(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    language = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='books', limit_choices_to={'is_verified_author': True})
    category = models.ManyToManyField(Category, related_name='category_book')

    def __str__(self) -> str:
        return f'{self.name} by {self.author.user.first_name}'
    
class Comment(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()