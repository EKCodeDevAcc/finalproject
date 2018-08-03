from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("list", views.listView, name="list"),
    path("searchList", views.searchList, name="search_list")
]