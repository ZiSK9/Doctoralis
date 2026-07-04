from django.db import models

# Create your models here.
class login_doyen(models.Model):
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.username

    def authenticate(self, provided_username, provided_password):
        return self.username == provided_username and self.password == provided_password