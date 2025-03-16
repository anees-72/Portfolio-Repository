from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makelisting", views.makelisting, name="makelisting"),
    path("listingdetails/<int:listing_id>", views.listingdetails, name="listingdetails"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category")
]
