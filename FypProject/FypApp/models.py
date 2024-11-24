from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)  # Example max_length constraint
    email = models.EmailField(max_length=100, unique=True, validators=[EmailValidator()])  # Email validation
    password = models.CharField(max_length=16, validators=[MinLengthValidator(8)])  # Password with minimum length constraint



class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='images/', null=False)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.title