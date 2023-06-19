from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    cat = models.CharField(max_length=40)

    def __str__(self):
        return self.cat

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")


class Listings(models.Model):
    title = models.CharField(max_length=64)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    description = models.CharField(max_length=300)
    listing_creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="creator")
    img = models.CharField(max_length=900)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    creation_date = models.DateTimeField(default=timezone.now)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="item")
    comment_text = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
