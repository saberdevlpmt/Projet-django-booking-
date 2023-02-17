from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

# Create your models here.
class User(AbstractUser):
    nom = models.CharField(max_length=30)    
    adresse = models.TextField()
    email = models.EmailField(unique=True)
    numero_de_telephone = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group, related_name='users')
    user_permissions = models.ManyToManyField(Permission, related_name='users')
    
class Event(models.Model):    
    date = models.DateField()
    time = models.TimeField()
    commentaires = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
    
     