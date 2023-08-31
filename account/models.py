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
        return self.user.username