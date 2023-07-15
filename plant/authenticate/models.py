from django.db import models

from django.contrib.auth.models import User


# Create your models here.




class otp_generation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)
    tokens = models.CharField(max_length=10)
