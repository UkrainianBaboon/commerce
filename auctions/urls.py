from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("lot/<str:id>", views.lot, name="lot"),
    path("create", views.create_lot, name="create"),
    path("save", views.save_lot, name="save_lot"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bet/<str:id>", views.bet, name="bet"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<str:title>", views.category_item, name="category_item")

]
