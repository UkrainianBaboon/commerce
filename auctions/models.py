from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField

# from auctions.views import watchlist


class User(AbstractUser):
    def __str__(self):
        return self.username

class Category(models.Model):
    category_title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_title}"
    
class Bet(models.Model):
    bet = models.FloatField()
    
    def __str__(self):
        return f"{self.bet}"
    
class Lot(models.Model):
    title = models.CharField(max_length=64)
    description  = models.TextField(max_length=512)
    first_bet = models.IntegerField()
    photo = models.URLField(max_length=200, blank=True)
    category = models.ManyToManyField(Category, related_name="lots")
    author = models.ForeignKey(User, default="1", on_delete=CASCADE, related_name="lot")
        
    
    def __str__(self):
        return f"Лот №{self.pk} - {self.title}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="list")
    lot = models.ManyToManyField(Lot, related_name="user")
    def __str__(self):
        return f"{self.id}) {self.user}"

class Comment(models.Model):
    pass

