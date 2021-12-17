from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.db.utils import Error
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

import auctions

# import auctions


from .models import Bet, Comment, User, Lot, Category, Watchlist

class NewLotForm(ModelForm):
    class Meta:
        model = Lot
        fields = ["title", "description", "first_bet", "photo", "category"]
        labels = {
            'title': ('Назва'),
            'description': ('Опис'),
            'first_bet': ('Початкова ціна'),
            'photo': ('Фото'),
            'category': ('Категорія')
        }
class WatchListForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["lot"]

class NewBetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ["bet"]
        labels = {
            "bet": ('Ваша ставка')
        }
class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        labels = {
            "comment": ('Напишіть коментар')
        }

def index(request):
    bets = Bet.objects.all()
    return render(request, "auctions/index.html",{
        "lots": Lot.objects.all(),
        "bets": bets
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Ім'я користувача або пароль невірні."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Паролі не співпадають."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Користувача з таким ім'ям вже зареєстровано."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required (login_url="login")
def lot(request, id):

    lot = Lot.objects.get(pk=id)
    categories = Category.objects.filter(lots=id)
    user = User.objects.get(username=request.user)
    bets = Bet.objects.filter(lot=id)
    comments = Comment.objects.filter(lot=id)
    winner = None
    sold = True
    if len(bets) >= 1:
        max_bet = bets[len(bets)-1].bet
        winner = bets[len(bets)-1].client
    else:
        max_bet = lot.default_bet
        sold = False
    if lot.first_bet != max_bet:
        lot.first_bet = max_bet
        lot.save()
    if not user.list.filter(lot=lot):
        watched = True
    else:
        watched = False
    if request.method == "POST":
        if request.POST.get("button")== "Відстежувати лот":
            watchlist = Watchlist()
            watchlist.lot = lot
            watchlist.user = user
            watchlist.save()
        else:
            watchlist = Watchlist.objects.filter(user=user)
            watchlist.get(lot=lot).delete()
            
        return HttpResponseRedirect(reverse ("watchlist"))   
                
    else:
        return render(request, "auctions/lot.html", {
            "lot": lot,
            "bets": bets,
            "categories": categories,
            "id": id,
            "watched": watched,
            "max_bet": max_bet,
            "new_bet_form": NewBetForm,
            "user": user,
            "sold": sold,
            "new_comment_form": NewCommentForm,
            "comments": comments,
            "winner": winner
            
        })
        


@login_required (login_url="login")
def create_lot(request):
    if request.method == "POST":
        form = NewLotForm(request.POST)
        user = User.objects.get(username=request.user)
        if form.is_valid:
            new_lot = form.save()
            new_lot.author = user
            new_lot.default_bet = new_lot.first_bet
            new_lot.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "form": NewLotForm()
        })
    
def save_lot(request):
    form = NewLotForm(request.POST)
    if form.is_valid:
        form.description = request.POST.get('new_lot_title')
        form.description = request.POST.get('new_lot_description')
        form.photo = request.POST.get("new_lot_photo")
        form.first_bet = request.POST.get("new_lot_first_bet")
        form.save()
    return HttpResponseRedirect(reverse ("index"))



    
@login_required (login_url="login")
def watchlist(request):
    user = User.objects.get(username=request.user)
    watchlist = Watchlist.objects.filter(user=user)
    # if request.method == "POST":
    #     watchlist = Watchlist.objects.get(id=nick.id)
    #     form = WatchListForm(request.POST, instance=watchlist)
    #     new_item = form.fields
    #     new_items = form.fields
        

    #     if form.is_valid():                        
    #         watchlist.lot.add(new_item)
    #         watchlist.save()
    #     return HttpResponseRedirect(reverse ("watchlist"))
        
    # else:
    return render(request, "auctions/watchlist.html",{
        "nick": user,
        "lots": watchlist
})
@login_required (login_url="login")
def bet(request, id):
    lot = Lot.objects.get(pk=id)
    form = NewBetForm(request.POST)
    user = User.objects.get(username=request.user)
    if form.is_valid:
        if not request.POST.get("bet"):
            pass
        elif int(request.POST.get("bet")) <= lot.first_bet:
            return render(request, "auctions/not_enough_error.html",{
                "lot": lot,
                "id": id
            })
        else:
            new_bet = form.save()
            new_bet.lot = lot
            new_bet.bet = request.POST.get("bet")
            lot.first_bet = new_bet.bet
            new_bet.client = user
            new_bet.save()
            lot.save()
    
    return redirect("lot", id=id)

@login_required (login_url="login")
def close(request, id):
    lot = Lot.objects.get(pk=id)
    if lot.is_open == True:
        lot.is_open = False
        lot.save()
    else:
        lot.is_open = True
        lot.save()
    return redirect("lot", id=id)

@login_required (login_url="login")
def comment(request, id):
    lot = Lot.objects.get(pk=id)
    form = NewCommentForm(request.POST)
    user = User.objects.get(username=request.user)
    if form.is_valid:
        if not request.POST.get("bet"):
            pass
        else:
            new_comment = form.save()
            new_comment.lot = lot
            new_comment.comment = request.POST.get("comment")
            new_comment.user = user
            new_comment.save()
        return redirect("lot", id=id)
    
def category(request):
    categories = Category.objects.all()
    return render (request, "auctions/categories_list.html",{
        "categories": categories
    })
    
def category_item(request, title):
    lot = Lot.objects.all()
    if title == "guns":
        lot = lot.filter(category=1)
        category = "Зброя"
    elif title == "horses":
        lot = lot.filter(category=2)
        category = "Коні"
    elif title == "clothes":
        lot = lot.filter(category=3)
        category = "Одяг"
    elif title == "tobacco":
        category = "Тютюнові вироби"
        lot = lot.filter(category=4)
    elif title == "cows":
        lot = lot.filter(category=5)
        category = "Рогата худоба"
    elif title == "comunication-devices":
        lot = lot.filter(category=6)
        category = "Засоби зв'язку"
    elif title == "apes":
        category = "Примати"
        lot = lot.filter(category=7)
    elif title == "food-and-drinks":
        lot = lot.filter(category=8)
        category = "Їжа та напої"
    return render(request, "auctions/category.html",{
        "category": category,
        "lots": lot
    })