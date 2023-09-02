from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator



class User(AbstractUser):
    email = models.EmailField(unique=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18)])
    national_code = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f'{self.user.username}'
    
class Address(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f'{self.customer.user}'