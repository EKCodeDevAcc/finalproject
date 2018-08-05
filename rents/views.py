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


# Menu Page.
def listView(request):
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    # To distinguish items depends on their menu type and size, get multiple objects and passed.
    # cars_to_exclude = ['Toyota']
    reserved_ids = []

    enable_cars = Car.objects.exclude(id__in=reserved_ids).all()
    context = {
        'cars' : enable_cars
    }
    return render(request, 'rents/list.html', context)


# Search Result View
def searchView(request, startdate, enddate, location, sort):
    start_datetime = datetime.strptime(startdate, "%a, %d %b %Y %H:%M:%S %Z")
    end_datetime = datetime.strptime(enddate, "%a, %d %b %Y %H:%M:%S %Z")

    reserved_cars = ReservedDate.objects.filter(Q(reserved_date_start_date__range=[start_datetime, end_datetime])|Q(reserved_date_end_date__range=[start_datetime, end_datetime]))
    reserved_ids = [ids.reserved_date_car.id for ids in reserved_cars]

    if location == 'All':
        no_location_id = []
    else:
        no_location = Location.objects.exclude(location_name=location)
        no_location_id = [ids.id for ids in no_location]

    if sort == 'price_desc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('-car_price')
    elif sort == 'price_asc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('car_price')
    elif sort == 'size_desc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('-car_size')
    elif sort == 'size_asc':
        enable_cars = Car.objects.exclude(Q(id__in=reserved_ids)|Q(car_location__id__in=no_location_id)).all().order_by('car_size')

    context = {
        'cars' : enable_cars,
        'startdate' : startdate,
        'enddate' : enddate,
        'location' : location,
        'sort' : sort
    }
    return render(request, 'rents/search.html', context)


# Reservation View
def reservationView(request, carid, startdate, enddate):

    # Calculate the number of difference of two dates.
    date_form = "%m/%d/%Y"
    startdate_form = datetime.strptime(startdate, "%a, %d %b %Y %H:%M:%S %Z")
    enddate_form = datetime.strptime(enddate, "%a, %d %b %Y %H:%M:%S %Z")
    date_num = enddate_form - startdate_form

    # if no cars avaiable for that date, return error message

    car_info = Car.objects.filter(id=carid)

    context = {
        'carinfos' : car_info,
        'startdate' : startdate,
        'enddate' : enddate,
        'datenum' : date_num.days,
        'multipleprice' : date_num.days * car_info[0].car_price,
        'taxes' : date_num.days * car_info[0].car_price * 0.315,
        'totalprice' : date_num.days * car_info[0].car_price + date_num.days * car_info[0].car_price * 0.315,
    }
    return render(request, 'rents/reservation.html', context)


# Create Reservation and Reservation Date
def bookCar(request):
    car_id = request.GET.get('carid')
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    total_price = request.GET.get('totalprice')

    get_reservation_user = User.objects.filter(id=request.user.id)
    get_reservation_car = Car.objects.filter(id=car_id)

    startdate_form = datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S %Z")
    enddate_form = datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S %Z")

    latest_reservation = Reservation.objects.create(reservation_user=get_reservation_user[0], reservation_car=get_reservation_car[0],
    reservation_start_date=startdate_form, reservation_end_date=enddate_form, reservation_pick_up='Boston',
    reservation_drop_off='Boston', reservation_protection='No', reservation_total_price=total_price,
    reservation_status='Waiting', reservation_request='No')

    # Get id of reservation just booked.
    # latest_reservation_id = Reservation.objects.latest('id')

    ReservedDate.objects.create(reserved_date_car=get_reservation_car[0], reserved_date_reservation=latest_reservation,
    reserved_date_start_date=startdate_form, reserved_date_end_date=enddate_form)

    return JsonResponse({'order_stats': 'Complete'})