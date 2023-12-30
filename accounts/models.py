from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel
from .constants import GENDER_TYPE, ACCOUNT_TYPE
# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    is_verified_author = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'account no#{self.id} - Name: {self.user.first_name} {self.user.last_name} - created on: {self.created_at}'

class UserAddress(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return str(self.user.email)
