from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    pass

class Comment(Model):
    username=CharField(max_length=30, null=True)
    listing=CharField(max_length=30, null=True)
    message=TextField(null=True)

class Listing(Model):
    username=CharField(max_length=30, null=True)
    title=CharField(max_length=30)
    description=TextField()
    starting_bid=IntegerField()
    category=CharField(max_length=30, null=True)
    comment=ForeignKey(Comment, on_delete=CASCADE, related_name='listing_comment', null=True)
    image_url=CharField(max_length=2000, null=True)

class Inactive_Listng(Model):
    username=CharField(max_length=30, null=True)
    title=CharField(max_length=30)
    starting_bid=IntegerField()
    winning_bid=IntegerField(null=True)
    winning_user=CharField(max_length=30, null=True)
    description=TextField(null=True)

class Category(Model):
    title=CharField(max_length=30, null=True)
    category=CharField(max_length=30, null=True)
    listing_id=IntegerField(primary_key=True)

class Watchlist(Model):
    username=CharField(max_length=30, null=True)
    title=CharField(max_length=30)
    listing_id=IntegerField(primary_key=True)

class Bid(Model):
    username=CharField(max_length=30, null=True)
    bid=IntegerField()
    title=CharField(max_length=30)
    starting_bid=CharField(max_length=30)
    def __str__(self):
        return f'{self.username} {self.bid}'
