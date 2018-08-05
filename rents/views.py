from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
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
def reservationView(request):
    context = {
        'cars' : 'asd'
    }
    return render(request, 'rents/reservation.html', context)