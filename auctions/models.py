from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    pass

class Category(models.Model):
    category_title = models.CharField(max_length=64)

    def __str__(self):
        return self.category_title
    
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
        
    
    def __str__(self):
        return f"Лот №{self.pk} - {self.title}"



class Comment(models.Model):
    pass

