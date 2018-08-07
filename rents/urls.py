from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("search/<str:startdate>/<str:enddate>/<str:location>/<str:age>/<str:sort>", views.searchView, name="search"),
    path("reservation/<int:carid>/<str:startdate>/<str:enddate>/<str:age>", views.reservationView, name="reservation"),
    path("bookCar", views.bookCar, name="book_car"),
    path("history", views.historyView, name="history"),
    path("history/<int:reservationid>/<int:userid>", views.historyDetailView, name="history_detail"),
    path("requestCancellation", views.requestCancellation, name="request_cancellation"),
    path("adminpage/reservation/<str:time>/<str:status>", views.adminReservationView, name="admin_reservation"),
]