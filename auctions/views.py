from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

import auctions


from .models import User, Lot, Category

class NewLotForm(forms.Form):
    new_lot_title = forms.CharField(max_length=64, label="Назва лоту")
    new_lot_description  = forms.CharField(widget=forms.Textarea, max_length=512, label="Опис лоту")
    new_lot_first_bet = forms.IntegerField(label="Початкова ставка")
    new_lot_photo = forms.URLField(max_length=200, label="Фото")
    new_lot_category = Category.objects.all()


def index(request):
    return render(request, "auctions/index.html",{
        "lots": Lot.objects.all()
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
    
def lot(request, id):
    lot = Lot.objects.get(pk=id)
    return render(request, "auctions/lot.html", {
        # "id": id,
        "lot": lot
    })
    
def create_lot(request):
    return render(request, "auctions/create.html", {
        "creation_form": NewLotForm
    })
    
def save_lot(request):
    form = NewLotForm(request.POST)
    if form.is_valid:
        Lot.title = request.POST.get('new_lot_title')
        Lot.description = request.POST.get('new_lot_description')
        Lot.photo = request.POST.get("new_lot_photo")
        Lot.first_bet = request.POST.get("new_lot_first_bet")
    return HttpResponseRedirect(reverse ("index"))
                                