from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class User(AbstractUser):
    pass
class Listing(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    image = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User, on_delete=CASCADE, related_name="list_owner")
    current_bid = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
class Bids(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name="bid_owner")
    bidprice = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")

class Comments(models.Model):
    commentdescription = models.CharField(max_length=350)
    maker = models.ForeignKey(User, on_delete=CASCADE, related_name="comment_maker")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    listing=models.ForeignKey(Listing, on_delete=CASCADE, related_name="listing")
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="user_watchlist")
