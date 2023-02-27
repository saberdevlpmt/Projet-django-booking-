
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nom = models.CharField(max_length=30)    
    adresse = models.TextField()
    email = models.EmailField(unique=True)
    numero_de_telephone = models.CharField(max_length=20)
    
class Event(models.Model):
    date = models.DateField()
    time = models.TimeField()
    commentaires = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE , db_constraint=False)

    
    
    
    