from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mail(models.Model):
    Subject = models.TextField()
    Email = models.TextField()

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.Mail
    
class Event(models.Model):

    Eventname = models.TextField()

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.Event


