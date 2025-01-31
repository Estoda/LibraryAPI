from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile/", blank=True, null=True, default="profile/default.png"
    )
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    description = models.TextField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to="book/", blank=True, null=True, default="book/default.png"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
