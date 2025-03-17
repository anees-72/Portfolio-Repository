
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost",views.newpost, name="newpost"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("toggle_follow", views.toggle_follow, name="toggle_follow"),
    path("following", views.following, name="following"),
    #api routes
    path("edit_post", views.edit_post, name="edit_post"),
    path("toggle_like", views.toggle_like, name="toggle_like"),
]
