from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField
User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=150)
    group = models.CharField(max_length=150,null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey('Room',null=False,blank=False,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    message = models.TextField()

    def __str__(self):
        return self.message