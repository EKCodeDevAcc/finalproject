from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from datetime import datetime
from django.apps import apps

from .models import Location, Car, Reservation, ReservedDate, Request
from .forms import UserSignUpForm

# Create your views here.
def index(request):
    # If user is not logged in, redirect him/her to login page.
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html')
    # Display all locations.
    location = Location.objects.all()
    context = {
        'locations' : location
    }
    return render(request, 'rents/index.html', context)

# Sign Up Page.
def signUp(request):
    # If user is logged in, redirect him/her to main page with message.
    if request.user.is_authenticated:
        return render(request, 'rents/index.html', {'message': 'To sign up, you have to logout first.'})
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserSignUpForm()
    return render(request, 'rents/sign_up.html', {'form': form})

# Login Page.
def loginView(request):
    if request.user.is_authenticated:
        return render(request, 'rents/index.html', {'message': 'You already logged in.'})
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'rents/login.html', {'message': 'Invalid credentials.'})

# Logout
def logoutView(request):
    logout(request)
    return render(request, 'rents/login.html', {'message': 'You are logged out successfully.'})

# Error Page.
def errorView(request):
    if request.user.is_authenticated:
        return render(request, 'rents/index.html', {'message': 'You already logged in.'})
    return render(request, 'rents/error.html')

# Search Result View
def searchView(request, startdate, enddate, location, age, sort):
    if not request.user.is_authenticated:
        return render(request, 'rents/index.html', {'message': 'Please login first.'})
    start_datetime = datetime.strptime(startdate, "%a, %d %b %Y %H:%M:%S %Z")
    end_datetime = datetime.strptime(enddate, "%a, %d %b %Y %H:%M:%S %Z")
    reserved_cars = ReservedDate.objects.filter(Q(reserved_date_start_date__range=[start_datetime, end_datetime])|Q(reserved_date_end_date__range=[start_datetime, end_datetime]))
    reserved_ids = [ids.reserved_date_car.id for ids in reserved_cars]

    # Display all cars or cars from certain location.
    if location == 'All':
        no_location_id = []
    else:
        no_location = Location.objects.exclude(location_name=location)
        no_location_id = [ids.id for ids in no_location]

    # Different order depends on order type.
    if sort == 'price_desc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('-car_price')
    elif sort == 'price_asc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('car_price')
    elif sort == 'size_desc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('-car_size')
    elif sort == 'size_asc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('car_size')

    # Get the number of cars meet the condition.
    result_length = len(Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all())

    context = {
        'cars' : enable_cars,
        'startdate' : startdate,
        'enddate' : enddate,
        'location' : location,
        'age' : age,
        'sort' : sort,
        'resultlength' : result_length
    }
    return render(request, 'rents/search.html', context)

# Reservation View
def reservationView(request, carid, startdate, enddate, age):
    if not request.user.is_authenticated:
        return render(request, 'rents/index.html', {'message': 'Please login first.'})
    # Calculate the number of difference of two dates.
    date_form = "%m/%d/%Y"
    startdate_form = datetime.strptime(startdate, "%a, %d %b %Y %H:%M:%S %Z")
    enddate_form = datetime.strptime(enddate, "%a, %d %b %Y %H:%M:%S %Z")
    date_diff = enddate_form - startdate_form
    date_num = date_diff.days

    # if no cars avaiable for that date, return error message

    car_info = Car.objects.filter(id=carid)
    multipe_price = date_num * car_info[0].car_price
    round_multipe_price = round(multipe_price,2)

    # Uner 25 users, 33% extra young rental fee.
    if age == 'Under':
        young_fee = date_num * car_info[0].car_price * 0.33
        round_young_fee = round(young_fee,2)
    elif age == 'Over':
        round_young_fee = 0
    taxes = (round_multipe_price + round_young_fee) * 0.0625
    round_taxes = round(taxes,2)
    total_price = round_multipe_price + round_young_fee + round_taxes

    location_list = Location.objects.all()

    context = {
        'carinfos' : car_info,
        'startdate' : startdate,
        'enddate' : enddate,
        'datenum' : date_num,
        'multipleprice' : round_multipe_price,
        'youngfee' : round_young_fee,
        'taxes' : round_taxes,
        'totalprice' : total_price,
        'locationlists' : location_list
    }
    return render(request, 'rents/reservation.html', context)

# Create Reservation and Reservation Date
def bookCar(request):
    car_id = request.GET.get('carid')
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    total_price = request.GET.get('totalprice')
    protection = request.GET.get('protection')
    dropoff = request.GET.get('dropoff')

    get_reservation_user = User.objects.filter(id=request.user.id)
    get_reservation_car = Car.objects.filter(id=car_id)

    startdate_form = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S %Z")
    enddate_form = datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S %Z")

    get_reservation_drop_off = Location.objects.filter(location_name=dropoff)

    # Get the reservation just booked.
    latest_reservation = Reservation.objects.create(reservation_user=get_reservation_user[0], reservation_car=get_reservation_car[0],
        reservation_start_date=startdate_form, reservation_end_date=enddate_form, reservation_drop_off=get_reservation_drop_off[0],
        reservation_protection=protection, reservation_total_price=total_price, reservation_status='Waiting', reservation_request='No')

    ReservedDate.objects.create(reserved_date_car=get_reservation_car[0], reserved_date_reservation=latest_reservation,
    reserved_date_start_date=startdate_form, reserved_date_end_date=enddate_form)

    return JsonResponse({'order_stats': 'Complete'})

# My History Page.
def historyView(request):
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    # Get a list of reservation where its user id matches with current user id.
    my_reservation = Reservation.objects.filter(reservation_user__id=request.user.id).all()

    context = {
        'myreservations' : my_reservation
    }
    return render(request, 'rents/history.html', context)

# My History Detail Page
def historyDetailView(request, reservationid, userid):
    reservation_detail = Reservation.objects.filter(id=reservationid).all()
    reservation_length = len(reservation_detail)
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    elif not userid == request.user.id:
        return render(request, 'rents/error.html', {'message': 'You have no access to this page.'})
    elif reservation_length == 0:
        return render(request, 'rents/error.html', {'message': 'No Result.'})
    else:
        context = {
            'reservationdetails' : reservation_detail
        }
        return render(request, 'rents/history_detail.html', context)

# Cancellation Request
def requestCancellation(request):
    reservation_id = request.GET.get('reservationid')
    reservation_drop_off = request.GET.get('reservationdropoff')

    # Existed reservation
    old_selected_reservation = Reservation.objects.filter(id=reservation_id)

    # Update its reservation request from no to yes
    selected_reservation = Reservation.objects.filter(id=reservation_id).update(reservation_request='Yes')

    startdate_form = old_selected_reservation[0].reservation_start_date
    enddate_form = old_selected_reservation[0].reservation_end_date

    # Existed reserved date
    selected_reserved_date = ReservedDate.objects.filter(reserved_date_reservation__id=reservation_id)
    get_reservation_drop_off = Location.objects.filter(location_name=reservation_drop_off)

    Request.objects.create(request_reservation=old_selected_reservation[0], request_reserved_date=selected_reserved_date[0],
        request_start_date=startdate_form, request_end_date=enddate_form, request_drop_off=get_reservation_drop_off[0],
        request_status='Cancellation', request_approval='Waiting')

    return JsonResponse({'order_stats': 'Complete'})