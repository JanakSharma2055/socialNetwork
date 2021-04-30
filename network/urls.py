
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following",views.Following,name="following"),
    path("profile/<str:user_name>",views.profileView,name="profile"),
    path("edit",views.editPost,name="editPost")
]

