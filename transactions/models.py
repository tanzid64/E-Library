from django.db import models
from accounts.models import Profile
from core.models import BaseModel
from book.models import Book
from .constants import TRANSACTION_TYPE
# Create your models here.
class Transaction(BaseModel):
    profile = models.ForeignKey(Profile, related_name = 'transactions', on_delete = models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    # balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null = True) 
    book = models.ManyToManyField(Book, related_name='book_transactions')
    class Meta:
        ordering = ['created_at']