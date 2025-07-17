from django.db import models
from django.utils import timezone


class Users(models.Model):
   username= models.CharField(max_length=20, unique=True)
   email = models.EmailField(unique=True)
   phone_number = models.CharField(max_length=15, unique=True)
   password = models.CharField(max_length=11)



def __str__(self):
        return self.username

class LoginToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

def __str__(self):
         return f"{self.user.username} - {self.token}"