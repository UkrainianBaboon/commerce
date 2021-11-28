from django.contrib import admin
from .models import Bet, Category, Comment, Lot, User

# Register your models here.

admin.site.register(User)
admin.site.register(Lot)
admin.site.register(Bet)
admin.site.register(Comment)
admin.site.register(Category)