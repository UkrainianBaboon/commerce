from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.forms.models import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

import auctions


from .models import User, Lot, Category

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


def index(request):
    return render(request, "auctions/index.html",{
        "lots": Lot.objects.all()})


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
    categories = Category.objects.filter(lots=id)
        
    return render(request, "auctions/lot.html", {
        # "id": id,
        "lot": lot,
        "categories": categories
        # "category": Lot.objects.get(category=id)
    })

@login_required(login_url='auctions/login.html')
def create_lot(request):
    return render(request, "auctions/create.html", {
        "creation_form": NewLotForm
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
                                