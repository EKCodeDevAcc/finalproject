from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

import datetime
from dateutil import parser

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
    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')

    print(start_date)
    print(type(start_date))

    pystart = dt.parse(start_date)
    print(pystart)
    print(type(pystart))

    # cars_to_exclude = ['Toyota']
    # cars_to_exclude = ReservedDate.objects.filter(Q(reserved_date_start_date__range(datetime(start_date),datetime(end_date))))|Q(reserved_date_end_date__range(datetime(start_date),datetime(end_date))).all()
    cars_to_exclude = ReservedDate.objects.filter(reserved_date_start_date=start_date)

    print('HIHI')
    print(cars_to_exclude)

    car = Car.objects.exclude(car_brand__in=cars_to_exclude).all()
    context = {
        'cars' : car
    }
    return render(request, 'rents/list.html', context)