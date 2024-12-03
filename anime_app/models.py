from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Model for storing user prefrences

class UserPreference(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    favorite_genres= models.JSONField(default=list)
    watched_anime= models.JSONField(default=list)

    def __str__(self):
        return f"Preferences of {self.user.username}"