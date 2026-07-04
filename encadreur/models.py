from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Encadreur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_prenom = models.CharField(max_length=100, null=True)
    validation = models.BooleanField(default=False) 


    def __str__(self):
        return self.user.username
