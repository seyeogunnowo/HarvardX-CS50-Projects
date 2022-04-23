from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    followers=IntegerField(default=0)
    following=IntegerField(default=0)


class Post(Model):
    username=CharField(max_length=200, null=True)
    content=TextField(null=True)
    date=DateTimeField(null=True, auto_now_add=True)
    like=IntegerField(default=0)

    def serialize(self):
        return{
        'id':self.id,
        'username':self.username,
        'content':self.content,
        'like':self.like,
        'date':self.date,
        }

class Post_Following(Model):
    user=CharField(max_length=200, null=True)
    username=CharField(max_length=200, null=True)
    content=TextField(null=True)
    date=DateTimeField(null=True, auto_now_add=True)
    like=IntegerField(default=0)
    def serialize(self):
        return{
        'id':self.id,
        'user':self.user,
        'username':self.username,
        'content':self.content,
        'like':self.like,
        'date':self.date,
        }
class User_Following(Model):
    user=CharField(max_length=200, null=True)
    username=CharField(max_length=200, null=True)

class Like(Model):
    user=CharField(max_length=200, null=True)
    post=ManyToManyField("Post", related_name="posts_liked")
    def serialize(self):
        return{
        'id':self.id,
        'user':self.user,
        'post':[self.post],
        }
