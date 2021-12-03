from django.contrib import admin
from .models import Bet, Category, Comment, Lot, User, Watchlist

# Register your models here.

admin.site.register(User)
admin.site.register(Lot)
admin.site.register(Bet)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Watchlist)