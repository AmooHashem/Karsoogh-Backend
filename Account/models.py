from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        Male = 'Male'
        Female = 'Female'

    phone_number = models.CharField(max_length=15, blank=False, null=False)
    backup_phone_number = models.CharField(max_length=15, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=Gender.choices)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)


class Student(models.Model):
    class Grade(models.TextChoices):
        First = 'First'
        Second = 'Second'
        Third = 'Third'
        Forth = 'Forth'
        Fifth = 'Fifth'
        Sixth = 'Sixth'
        Seventh = 'Seventh'
        Eighth = 'Eighth'
        Ninth = 'Ninth'
        Tenth = 'Tenth'
        Eleventh = 'Eleventh'
        Twelfth = 'Twelfth'

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    grade = models.CharField(choices=Grade.choices, max_length=10, null=True, blank=True)
    school = models.ForeignKey('School', on_delete=models.PROTECT, null=True, blank=True)


class School(models.Model):
    class SchoolType(models.Choices):
        Elementary = 'Elementary'
        Junior = 'Junior'
        High = 'High'

    type = models.CharField(choices=SchoolType.choices, max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    manager_name = models.CharField(max_length=50, null=True, blank=True)
    manager_phone_number = models.CharField(max_length=15, null=True, blank=True)

    province = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)


class Buyable(models.Model):
    pass
