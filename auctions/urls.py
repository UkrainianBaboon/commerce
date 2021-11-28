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
]
