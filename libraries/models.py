from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Library(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=600)
    location = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name = 'libraries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=400)
    authors = models.CharField(max_length=400)
    notes = models.CharField(max_length=4000, null=True, blank=True)
    library = models.ForeignKey(Library, on_delete=models.PROTECT, related_name = 'Books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

