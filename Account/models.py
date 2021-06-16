from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.


class User(AbstractBaseUser):
    class Gender(models.TextChoices):
        Male = 'Male'
        Female = 'Female'
