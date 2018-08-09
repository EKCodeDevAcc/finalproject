from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signUp", views.signUp, name="signUp"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("search/<str:startdate>/<str:enddate>/<str:location>/<str:age>/<str:sort>", views.searchView, name="search"),
    path("search/<str:startdate>/<str:enddate>/<str:location>/<str:age>/<str:sort>/<str:keytype>/<str:keyword>", views.searchKeywordView, name="search_keyword"),
    path("reservation/<int:carid>/<str:startdate>/<str:enddate>/<str:age>", views.reservationView, name="reservation"),
    path("bookCar", views.bookCar, name="book_car"),
    path("history", views.historyView, name="history"),
    path("history/<int:reservationid>/<int:userid>", views.historyDetailView, name="history_detail"),
    path("requestCancellation", views.requestCancellation, name="request_cancellation"),
    path("adminpage/reservation/<str:time>/<str:status>", views.adminReservationView, name="admin_reservation"),
    path("adminpage/reservation/<int:reservationid>", views.adminReservationDetailView, name="admin_reservation_detail"),
    path("reservationStatus", views.reservationChange, name="reservation_change"),
    path("adminpage/request/<str:time>/<str:status>", views.adminRequestView, name="admin_request"),
    path("adminpage/request/<int:requestid>", views.adminRequestDetailView, name="admin_request_detail"),
    path("requestApproval", views.requestApproval, name="request_approval")
]