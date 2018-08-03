from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.db.models import Q

import datetime

from .models import Car, Reservation, ReservedDate, Request
from .forms import UserSignUpForm

# Create your views here.
def index(request):
    # If user is not logged in, redirect him/her to login page.
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html')
    return render(request, 'rents/index.html')

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
    # car = Car.objects.filter(car_type='Toyota').only('id')


    # regular_pizza_menu = Menu.objects.filter(menu_type='Regular Pizza', menu_size='Small').only('menu_name')

    # asd = ReservedDate.objects.filter(id=1).only('id')
    # print('asd')
    # print(asd)

    cars_to_exclude = ['Toyota']
    # cars_to_exclude = ReservedDate.objects.filter(Q(reserved_date_start_date__range(datetime(start_date),datetime(end_date))))|Q(reserved_date_end_date__range(datetime(start_date),datetime(end_date))).all()

    car = Car.objects.exclude(car_brand__in=cars_to_exclude).all()
    context = {
        'cars' : car
    }
    return render(request, 'rents/list.html', context)

def searchList(request):
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    start_datetime = datetime.datetime.strptime(start_date, "%a, %d %b %Y %H:%M:%S %Z")
    end_datetime = datetime.datetime.strptime(end_date, "%a, %d %b %Y %H:%M:%S %Z")
    reserved_cars = ReservedDate.objects.filter(Q(reserved_date_start_date__range=[start_datetime, end_datetime])|Q(reserved_date_end_date__range=[start_datetime, end_datetime]))
    reserved_ids = [ids.reserved_date_car.id for ids in reserved_cars]
    enable_cars = Car.objects.exclude(id__in=reserved_ids).all()
    cars_response = serializers.serialize("json", enable_cars)
    return HttpResponse(cars_response, content_type='application/json')