from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.fields import CharField
from django.db.models.fields.related import ManyToManyField
from django.urls import reverse
User = get_user_model()


class CodeQuery(models.Model):
    code = models.TextField()
    result = models.TextField(null=True)
    last_updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)


class Message(models.Model):
    room = models.ForeignKey(Group,null=False,blank=False,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    message = models.TextField()
    sended_at = models.DateTimeField(auto_now_add=True)
    isCodeQuery = models.BooleanField(default=False)
    codeQuery = models.OneToOneField(CodeQuery,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.message

def get_absolute_url(self):
    return reverse('join-room',args=[self.name])

Group.add_to_class('get_absolute_url',get_absolute_url)
User.add_to_class('online',models.BooleanField(default=False))