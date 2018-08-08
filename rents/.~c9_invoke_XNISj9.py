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
from django.contrib.auth.decorators import user_passes_test

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
    reserved_cars = ReservedDate.objects.filter((Q(reserved_date_start_date__range=[start_datetime, end_datetime])|Q(reserved_date_end_date__range=[start_datetime, end_datetime]))&~Q(reserved_date_reservation__reservation_status='Canceled'))
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

    # Check if this car already has a reservation for selected date.
    reserved_car_length = ReservedDate.objects.filter((Q(reserved_date_start_date__range=[startdate_form, enddate_form])|Q(reserved_date_end_date__range=[startdate_form, enddate_form]))&~Q(reserved_date_reservation__reservation_status='Canceled')&Q(reserved_date_car__id=carid)).count()

    if reserved_car_length > 0:
        return render(request, 'rents/error.html', {'message': 'This car is not available for selected date.'})
    else:
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
    # To check requested user is the owner of the reservation.
    reservation_detail = Reservation.objects.filter(Q(id=reservationid)&Q(reservation_user__id=request.user.id)).all()
    reservation_length = len(reservation_detail)
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    elif not userid == request.user.id:
        return render(request, 'rents/error.html', {'message': 'You have no access to this page.'})
    elif reservation_length == 0:
        return render(request, 'rents/error.html', {'message': 'No Result.'})
    else:
        reservation_request = Request.objects.filter(request_reservation__id=reservationid).all()
        context = {
            'reservationdetails' : reservation_detail,
            'reservationrequests' : reservation_request
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


# Admin page for check reservations
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminReservationView(request, time, status):
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    current_time = datetime.now()
    # Display past reservations.
    if time == 'past':
        reservation_list = Reservation.objects.filter(reservation_end_date__lt=current_time).all()
        search_status = 'past'
    elif time == 'current':
        # Display current waiting reservations.
        if status == 'waiting':
            reservation_list = Reservation.objects.filter(Q(reservation_end_date__gt=current_time)&Q(reservation_status='Waiting')).all()
            search_status = 'currentwait'
        # Display current checked-in reservations.
        elif status == 'checked':
            reservation_list = Reservation.objects.filter(Q(reservation_end_date__gt=current_time)&Q(reservation_status='Checked-in')).all()
            search_status = 'currentcheck'
        # Display current checked-in, complete, canceled reservations.
        elif status == 'complete':
            reservation_list = Reservation.objects.filter(Q(reservation_end_date__gt=current_time)&(Q(reservation_status='Complete')|Q(reservation_status='Canceled'))).all()
            search_status = 'currentcomplete'

    context = {
        'reservationlists' : reservation_list,
        'searchstatus' : search_status
    }
    return render(request, 'rents/admin_reservation.html', context)

# Admin Reservation Detail Page
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminReservationDetailView(request, reservationid):
    # To check requested user is the owner of the reservation.
    reservation_detail = Reservation.objects.filter(id=reservationid).all()
    reservation_length = len(reservation_detail)
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    elif reservation_length == 0:
        return render(request, 'rents/error.html', {'message': 'No Result.'})
    else:
        reservation_request = Request.objects.filter(request_reservation__id=reservationid).all()
        context = {
            'reservationdetails' : reservation_detail,
            'reservationrequests' : reservation_request
        }
        return render(request, 'rents/admin_reservation_detail.html', context)

# Admin page for check reservations
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminRequestView(request, time, status):
    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    current_time = datetime.now()
    # Display past reservations.
    if time == 'past':
        request_list = Request.objects.filter(request_reservation__reservation_end_date__lt=current_time).all()
        search_status = 'past'
    elif time == 'current':
        # Display current waiting reservations.
        if status == 'waiting':
            request_list = Request.objects.filter(Q(request_reservation__reservation_end_date__gt=current_time)&Q(request_approval='Waiting')).all()
            search_status = 'currentwait'
        # Display current checked-in reservations.
        elif status == 'declined':
            request_list = Request.objects.filter(Q(request_reservation__reservation_end_date__gt=current_time)&Q(request_approval='Declined')).all()
            search_status = 'currentdeclined'
        # Display current checked-in, complete, canceled reservations.
        elif status == 'approved':
            request_list = Request.objects.filter(Q(request_reservation__reservation_end_date__gt=current_time)&Q(request_approval='Approved')).all()
            search_status = 'currentapproved'

    context = {
        'requestlists' : request_list,
        'searchstatus' : search_status
    }
    return render(request, 'rents/admin_request.html', context)

# Admin Request Detail Page
# Limited to superuser
@user_passes_test(lambda user: user.is_superuser)
def adminRequestDetailView(request, requestid):
    # To check requested user is the owner of the reservation.
    request_detail = Request.objects.filter(id=requestid).all()
    request_length = len(request_detail)

    if not request.user.is_authenticated:
        return render(request, 'rents/login.html', {'message': 'Please login first.'})
    elif request_length == 0:
        return render(request, 'rents/error.html', {'message': 'No Result.'})
    else:
        context = {
            'requestdetails' : request_detail
        }
        return render(request, 'rents/admin_request_detail.html', context)

# Request Approve or Decline
def requestApproval(request):
    request_id = request.GET.get('requestid')
    request_status = request.GET.get('requeststatus')

    request_detail = Request.objects.filter(id=request_id).all()

    # Get start, end date of request
    startdate_form = request_detail[0].request_start_date
    enddate_form = request_detail[0].request_end_date
    reservation_id = request_detail[0].request_reservation.id
    drop_off = request_detail[0].request_drop_off

    # Check if there are another reservation for requested date range.
    reserved_length = ReservedDate.objects.filter(Q(reserved_date_start_date__range=[startdate_form, enddate_form])|Q(reserved_date_end_date__range=[startdate_form, enddate_form])).count()

    if request_status == 'Decline':
        Request.objects.filter(id=request_id).update(request_approval='Declined')
        return JsonResponse({'message': 'Declined the request succesfully.'})
    else:
        # Existed reserved date
        if request_detail[0].request_status == 'Cancellation':
            Request.objects.filter(id=request_id).update(request_approval='Approved')
            Reservation.objects.filter(id=reservation_id).update(reservation_status='Canceled')
            return JsonResponse({'message': 'Approved the request succesfully. The reservation is canceled.'})
        else:
            if reserved_length > 1:
                Request.objects.filter(id=request_id).update(request_approval='Declined')
                return JsonResponse({'message': 'The request cannot be approved due to duplication, so it is declined.'})
            else:
                Request.objects.filter(id=request_id).update(request_approval='Approved')
                Reservation.objects.filter(id=reservation_id).update(reservation_start_date=startdate_form, reservation_end_date=enddate_form, reservation_drop_off=drop_off)
                return JsonResponse({'message': 'Approved the request succesfully. The reservation is updated'})