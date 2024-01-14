from django.db.models import Q
import uuid
from .models import Bus, Coach
from dateutil.parser import parse
import datetime
import json
import os
from django.http import JsonResponse
import json
from django.core import serializers
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from datetime import datetime
from decimal import Decimal, InvalidOperation
from bus.forms import ReservationForm, ProfileForm, ComplaintForm
from bus.EmailBackEnd import EmailBackEnd
from bus.models import CustomUser, TicketBooking, Coach, Route, PropularRoutes, Counter, District, Category, FAQ, TermsAndConditions, Profile, Bus, Seat, Booking, JourneyDateHistory, CancelTicket, BusStop, RoutePart, Tax, Payment, Company
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.conf import settings
from post_office import mail
from post_office.models import EmailTemplate
import math
from decimal import Decimal
import logging
import sys
import time
import re
import random
from django.shortcuts import render
from .models import District, Counter, feedback
from django.http import HttpResponseBadRequest
from datetime import date
from .models import BoardingPoint
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.mail import send_mail
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt
from textwrap import wrap
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, ListItem, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ListStyle
from django.core.files.base import ContentFile

from random import randint


def index(request):
    districts = District.objects.all().order_by('name')
    paginator = Paginator(districts, 64)  # 5 rows x 13 elements per row = 65
    district_chunks = [paginator.page(i)
                       for i in range(1, paginator.num_pages + 1)]
    return render(request, 'index.html', {'district_chunks': district_chunks})


def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "logininfo/login_page.html")


def ShowLoginPageuser(request):
    return render(request, "logininfo/login_user.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

        if cap_json['success'] == False:
            messages.error(request, "Invalid Captcha. Try Again.")
            return HttpResponseRedirect("show_login")

        email_or_phone = request.POST.get("email_or_phone")
        password = request.POST.get("password")

        # Check if the provided value is an email or phone number
        if '@' in email_or_phone:
            # User provided an email
            user = EmailBackEnd.authenticate(
                request, email=email_or_phone, password=password)
        else:
            # User provided a phone number
            user = EmailBackEnd.authenticate(
                request, phone_number=email_or_phone, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == 0:
                return HttpResponseRedirect('/root_home')
            elif user.user_type == 1:
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == 2:
                # Assuming staff_type is a ForeignKey in the CustomUser model
                staff_type = user.staff_type

                if staff_type is not None:
                    staff_type_name = staff_type.name
                    if staff_type_name == 'Inventory':
                        return HttpResponseRedirect(reverse("dashboard_inventory"))
                    elif staff_type_name == 'Accounts':
                        return HttpResponseRedirect(reverse("dashboard_accounts"))
                    # elif staff_type_name == 'hr':
                    #     return HttpResponseRedirect(reverse("dashboard_hr"))
                    # elif staff_type_name == 'software_engineer':
                    #     return HttpResponseRedirect(reverse("dashboard_software_engineer"))
                    # elif staff_type_name == 'worker':
                    #     return HttpResponseRedirect(reverse("dashboard_worker"))
                    else:
                        # Handle other staff types
                        return HttpResponseRedirect('/admin_home')
                else:
                    # Handle the case when staff_type is None
                    return HttpResponseRedirect('/admin_home')
            elif user.user_type == 3:
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("show_login_user")


# def doLogin(request):
#     if request.method != "POST":
#         return HttpResponse("<h2>Method Not Allowed</h2>")
#     else:
#         captcha_token = request.POST.get("g-recaptcha-response")
#         cap_url = "https://www.google.com/recaptcha/api/siteverify"
#         cap_secret = "6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
#         cap_data = {"secret": cap_secret, "response": captcha_token}
#         cap_server_response = requests.post(url=cap_url, data=cap_data)
#         cap_json = json.loads(cap_server_response.text)

#         if cap_json['success'] == False:
#             messages.error(request, "Invalid Captcha Try Again")
#             return HttpResponseRedirect("show_login")

#         email_or_phone = request.POST.get("email_or_phone")
#         password = request.POST.get("password")

#         # Check if the provided value is an email or phone number
#         if '@' in email_or_phone:
#             # User provided an email
#             user = EmailBackEnd.authenticate(
#                 request, email=email_or_phone, password=password)
#         else:
#             # User provided a phone number
#             user = EmailBackEnd.authenticate(
#                 request, phone_number=email_or_phone, password=password)

#         if user is not None:
#             login(request, user)
#             if user.user_type == 0:
#                 return HttpResponseRedirect('/root_home')
#             elif user.user_type == 1:
#                 return HttpResponseRedirect('/admin_home')
#             elif user.user_type == 2:
#                 user_permissions = user.get_all_permissions()
#                 print("User Type 2 Permissions:", user_permissions)
#                 return HttpResponseRedirect('/admin_home')
#             elif user.user_type == 3:
#                 return HttpResponseRedirect(reverse("index"))
#             # else:
#             #     return HttpResponseRedirect(reverse("index"))  # Handle other user types
#         else:
#             messages.error(request, "Invalid Login Details")
#             return HttpResponseRedirect("show_login")

def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("show_login")


def Testurl(request):
    return HttpResponse("Ok")


def signup_admin(request):
    return render(request, "logininfo/signup_admin_page.html")



def signup_customer(request):

    return render(request, "logininfo/signup_customer_page.html")


def signup_user(request):
    return render(request, "logininfo/signup_user_page.html")


def do_admin_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, user_type=1)
        user.save()
        messages.success(request, "Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))


def do_user_signup(request):
    if request.method == 'POST':
        # Retrieve form field data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")

        # Validate the input data
        errors = {}
        if not username:
            errors['username'] = "Username is required."
        if not email:
            errors['email'] = "Email is required."
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = "This email is already in use. Please choose another one."
        if not password:
            errors['password'] = "Password is required."
        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match. Please try again."
        if not address:
            errors['address'] = "Address is required."
        if not re.match(r'^(019|018|014|015|016)\d{8}$', phone_number):
            errors['phone_number'] = "Invalid phone number. Please enter a valid number."
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            errors['phone_number'] = "This phone number is already in use. Please choose another one."

        if errors:
            # There are validation errors, render the same template with the errors and the user's input data
            context = {
                'username': username,
                'email': email,
                'address': address,
                'phone_number': phone_number,
                'errors': errors,
            }
            return render(request, 'logininfo/signup_user_page.html', context)

        # All input data is valid, store form field data in session for later use
        request.session['admin_username'] = username
        request.session['admin_email'] = email
        request.session['admin_password'] = password
        request.session['admin_address'] = address
        request.session['admin_phone_number'] = phone_number

        # Generate and send OTP
        otp = str(random.randint(1000, 9999))
        url = f'http://sms.iglweb.com/api/v1/send?api_key=4451685776780151685776780&contacts=88{phone_number}&senderid=01844532630&msg={otp} is your activation code in IGL Bus Service.This code will expire in 2 Hours.For help,call:01958666999'
        response = requests.get(url)
        if response.status_code == 200:
            # Store OTP in session for validation
            request.session['admin_otp'] = otp
            print('OTP: ', otp)

            return redirect(reverse("otp_verification_Signup"))
        else:
            messages.error(request, "Failed to send OTP. Please try again.")
            return HttpResponseRedirect(reverse("show_login"))
    else:
        # The request is not a POST, render the empty form
        return render(request, 'logininfo/signup_user_page.html')


def otp_verification_Signup(request):
    if request.method == 'POST':
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get('admin_otp')

        if entered_otp == stored_otp:
            try:
                # Retrieve form field data from session
                username = request.session.get('admin_username')
                email = request.session.get('admin_email')
                password = request.session.get('admin_password')
                address = request.session.get('admin_address')
                phone_number = request.session.get('admin_phone_number')

                # Create the user and save form field data
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    phone_number=phone_number,
                    user_type=3
                )
                user.users.address = address
                user.save()

                # Clear session data
                del request.session['admin_otp']
                del request.session['admin_username']
                del request.session['admin_email']
                del request.session['admin_password']
                del request.session['admin_address']
                del request.session['admin_phone_number']

                messages.success(request, "Successfully Created Account")
                return HttpResponseRedirect(reverse("show_login"))
            except Exception as e:
                messages.error(request, f"Failed to Create Account: {str(e)}")
                return HttpResponseRedirect(reverse("show_login"))
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect(reverse("otp_verification_Signup"))
    else:
        return render(request, 'logininfo/otp_verification_signup.html')


def do_signup_customer(request):

    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")

    try:
        # Create a new CustomUser object
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email,
            user_type=3,
        )

        # Create a new Customers object and assign the admin field
        user.users.address = address
        user.save()
        messages.success(request, "Successfully Added Customer")
        return HttpResponseRedirect(reverse("show_login"))
    except Exception as e:
        messages.error(request, f"Failed to Add Customer: {str(e)}")
        return HttpResponseRedirect(reverse("show_login"))


@csrf_exempt
def seats_plan(request):
    if request.method == 'POST' and request.is_ajax():
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Reservation saved successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Error occurred while saving reservation.'})
    else:
        form = ReservationForm()
    return render(request, 'seats.html', {'form': form})

# 2nd page


def schedule(request):
    coach = Coach.objects.all()
    contex = {

        'coach': coach
    }
    return render(request, 'schedule.html', contex)

# search Bara


def search_bus(request):
    # Get the search query parameters from the request
    start_point = request.GET.get('start_point')
    end_point = request.GET.get('end_point')
    journey_date = request.GET.get('journey_date')

    # Query the Coach and Route models to find matching buses
    coaches = Coach.objects.filter(
        routes__start_point__icontains=start_point,
        routes__end_point__icontains=end_point,
        journeydate=journey_date
    )

    # Create a list of dictionaries containing the relevant bus data
    bus_data = []
    for coach in coaches:
        bus_data.append({
            'start_point': coach.routes.start_point,
            'end_point': coach.routes.end_point,
            'distance': coach.routes.distance,
            'travel_time': coach.routes.travel_time,
            'coach_number': coach.coachnumber,
            'coach_type': coach.coachtype,
            'coach_model_name': coach.coachmodelname,
            'arrival_time': coach.arrivaltime,
            'departure_time': coach.departuretime,
            'journey_date': coach.journeydate,
            'returndate': coach.returndate,
            'boarding_point': coach.boarding_point,

            'cancellation_policy': coach.cancellation_policy,
            'facilities': coach.facilities,
            'price': coach.price
        })

    # Create a dictionary of the search query parameters
    query_params = {
        'start_point': start_point,
        'end_point': end_point,
        'journey_date': journey_date,
        'bus_number': ''  # Placeholder for bus number
    }

    # Encode the query parameters into a URL query string
    encoded_query_params = urlencode(query_params)

    # Redirect to the search results page with the search query parameters in the URL
    redirect_url = reverse('search_results') + '?' + encoded_query_params
    return redirect(redirect_url)


def search_results(request):
    # Get the search query parameters from the URL
    start_point_name = request.GET.get('start_point')
    end_point_name = request.GET.get('end_point')
    bus_number = request.GET.get('bus_number')
    journey_date_str = request.GET.get('journey_date')
    journey_date = datetime.strptime(journey_date_str, '%d-%m-%Y').date()

    if request.user.is_authenticated:
        user = request.user
        company = user.company
        company = Company.objects.get(id=company.id)

    # Get BusStop objects for start_point and end_point
    start_point = get_object_or_404(
        BusStop, name__name__iexact=start_point_name)
    end_point = get_object_or_404(BusStop, name__name__iexact=end_point_name)

    # Get Coach objects for the given search criteria
    coaches = Coach.objects.filter(
        Q(routes__start_point=start_point) |
        Q(routes__end_point=end_point) |
        Q(routes__intermediate_stops=start_point) |
        Q(routes__intermediate_stops=end_point),
        journey_dates__journey_date=journey_date
    ).distinct()

    # Filter the RoutePart objects based on the start and end points
    route_parts = RoutePart.objects.filter(
        Q(coach__in=coaches),
        Q(start_point=start_point) & Q(end_point=end_point)
    )

    # Get the journey date history associated with the filtered route parts
    journey_date_history = JourneyDateHistory.objects.filter(
        journey_date=journey_date)

    # Create a list to store the prices for each RoutePart
    bus_data = []
    for route_part in route_parts:
        route = route_part.route
        coach = route_part.coach

        # Get the first journey date history instance for the coach matching the provided journey date
        journey_date_instance = journey_date_history.first()

        # Calculate the total seats and remaining seats for the given journey date
        total_seats, remaining_seats = Booking.get_booked_seats(
            journey_date=journey_date_instance.id if journey_date_instance else None, coach=coach, company=company)

        bus_data.append({
            'routes': route,
            'bus_number': coach.bus.bus_number,
            'start_point': route_part.start_point,
            'end_point': route_part.end_point,
            'distance': route.distance,
            'travel_time': route.travel_time,
            'coach_number': coach.coachnumber,
            'coach_type': coach.coachtype,
            'coach_model_name': coach.coachmodelname,
            'arrival_time': coach.arrivaltime,
            'departure_time': coach.depraturetime,
            'journey_date': journey_date,  # Pass the journey_date variable to the template
            'return_date': coach.returndate,
            'cancellation_policy': coach.cancellation_policy,
            'facilities': coach.facilities,
            'price': route_part.price,  # Price for the specific route part
            'remaining_seats': remaining_seats,
            'total_seats': total_seats
        })

    if not bus_data:
        message = 'No buses available for the selected route and date.'
        context = {'message': message}
    else:
        context = {
            'start_point': start_point,
            'end_point': end_point,
            'bus_data': bus_data,
            'journey_date': journey_date,  # Pass the journey_date variable to the template
        }

    # Render the search results template with the search query parameters and bus data
    return render(request, 'schedule.html', context)


def d_t_c_result(request, start_point, end_point):

    journey_date_str = request.GET.get('journey_date')
    journey_date = datetime.strptime(journey_date_str, '%d-%m-%Y').date()

    # Query the Coach and Route models to find matching buses
    coaches = Coach.objects.filter(
        routes__start_point__icontains=start_point,
        routes__end_point__icontains=end_point,
        journeydate=journey_date
    )

    # Create a list of dictionaries containing the relevant bus data
    bus_data = []
    for coach in coaches:
        bus_data.append({
            'routes': coach.routes,
            'start_point': coach.routes.start_point,
            'end_point': coach.routes.end_point,
            'distance': coach.routes.distance,
            'travel_time': coach.routes.travel_time,
            'coach_number': coach.coachnumber,
            'coach_type': coach.coachtype,
            'coach_model_name': coach.coachmodelname,
            'price': coach.price,
            'arrival_time': coach.arrivaltime,
            'departure_time': coach.depraturetime,
            'journey_date': coach.journey_dates.first(),
            'return_date': coach.returndate,

        })

    # Pass the search query parameters and bus data to the search results template
    context = {
        'start_point': start_point,
        'end_point': end_point,
        'journey_date': journey_date,
        'bus_data': bus_data,
    }

    # Render the search results template with the search query parameters and bus data
    return render(request, 'schedule.html', context)

# Popular Road


class PopularRoutesListView(ListView):
    model = PropularRoutes
    template_name = 'index.html'
    context_object_name = 'routes'


def popular(request):

    popular_routes = PropularRoutes.objects.all()
    start_point = request.GET.get('start_point')
    end_point = request.GET.get('end_point')

    try:
        popular_route = PropularRoutes.objects.get(
            route__start_point=start_point,
            route__end_point=end_point
        )
        fromdescription = popular_route.fromdescription
        todescription = popular_route.todescription
    except PropularRoutes.DoesNotExist:
        fromdescription = ''
        todescription = ''

    return render(request, 'routes/routes.html', {
        'start_point': start_point,
        'end_point': end_point,
        'fromdescription': fromdescription,
        'todescription': todescription,
    })


def Distract(request):
    districts = District.objects.all()
    context = {'districts': districts}
    return render(request, 'district_list.html', context)


# def counter_list(request, district):
#     counters = Counter.objects.filter(district__name=district)
#     context = {'counters': counters}
#     return render(request, 'counter_list.html', context)


# def counter_list_popup(request, district):
#     counters = Counter.objects.filter(district__name=district)
#     context = {'counters': counters}
#     return render(request, 'counter_list_popup.html', context)


# def counter_list_json(request, district_id):
#     district = get_object_or_404(District, id=district_id)
#     counters = Counter.objects.filter(district=district)
#     data = []
#     for counter in counters:
#         data.append({
#             'name': counter.name,
#             'latitude': counter.latitude,
#             'longitude': counter.longitude,
#         })
#     return JsonResponse({'counters': data})
def district_list(request):
    districts = District.objects.all()
    return render(request, 'counter_list.html', {'districts': districts})


def counter_list(request, district_id):
    district = get_object_or_404(District, pk=district_id)
    counters = district.counter_set.all()
    return render(request, 'counter_list.html', {'district': district, 'counters': counters})


def counter_detail(request, counter_id):
    counter = get_object_or_404(Counter, pk=counter_id)
    return render(request, 'counter_detail.html', {'counter': counter})
# About


def about(request):
    return render(request, 'about.html')


def cacelationpolicy(request):
    return render(request, 'cancelationpolicy.html')


def privacypolicy(request):
    return render(request, 'privacy.html')
# @api_view(['GET', 'POST'])
# def forget_password(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')

#         # Check if the number exists in the database
#         user = CustomUser.objects.filter(phone_number=phone_number).first()

#         if user:
#             # Generate OTP code
#             otp = random.randint(100000, 999999)

#             # Store OTP in session for the user
#             otp_data = {'code': otp, 'expiration_time': time.time() + 300}
#             request.session['otp_code'] = otp

#             # Send OTP code to the number using the SMS API
#             url = f'http://sms.iglweb.com/api/v1/send?api_key=4451683176096151683176096&contacts=88{phone_number}&senderid=8801844532630&msg=Bus Ticket Booking App OTP code is {otp}'
#             response = requests.get(url)

#             if response.status_code == 200:
#                 # Redirect to the OTP verification page
#                 return redirect(reverse("otp_verification") + f"?phone_number={phone_number}")
#             else:
#                 # Return JSON response with error message
#                 return JsonResponse({'success': False, 'message': 'Failed to send OTP code.'})
#         else:
#             # Return JSON response with error message
#             return JsonResponse({'success': False, 'message': 'Number not found in the database.'})

#     # Render forget password template if the request method is GET
#     return render(request, 'logininfo/forget_password.html')


# def otp_verification(request):

#     if request.method == 'GET':
#         phone_number = request.GET.get('phone_number')
#         return render(request, 'logininfo/otp_verification.html', {'phone_number': phone_number})

#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         entered_otp = request.POST.get('otp_code')

#         # Retrieve the OTP from the session for the user
#         session_otp = request.session.get('otp_code')

#         entered_otp = entered_otp.strip()

#         if session_otp is not None and entered_otp == str(session_otp):
#             # Remove the OTP from the session
#             del request.session['otp_code']
#             return redirect(f'/reset_password/?phone_number={phone_number}')
#         else:
#             # Return JSON response with error message
#             return JsonResponse({'success': False, 'message': 'Invalid OTP code.'})


# def reset_password(request):
#     if request.method == 'GET':
#         phone_number = request.GET.get('phone_number')
#         # Render the reset password template with the phone_number parameter
#         return render(request, 'logininfo/reset_password.html', {'phone_number': phone_number})

#     if request.method == 'POST':
#         phone_number = request.POST.get('phone_number')
#         new_password = request.POST.get('new_password')

#         # Reset the password for the user with the given phone number
#         try:
#             user = CustomUser.objects.get(phone_number=phone_number)
#             user.password = make_password(new_password)
#             user.save()
#             return JsonResponse({'success': True, 'message': 'Password reset successful.'})
#         except CustomUser.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'User not found.'})

#     # Render the password reset template
OTP_API_KEY = '4451683176096151683176096'
OTP_API_URL = f'http://sms.iglweb.com/api/v1/send?api_key={OTP_API_KEY}&contacts=88{{phone_number}}&senderid=8801844532630&msg=Bus Ticket Booking App OTP code is {{otp}}'


# Forget Password view
def forget_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Check if the phone number is registered
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            # Generate and send OTP to the user's phone number
            otp = generate_otp(phone_number)
            # Save the OTP and phone number in the session
            request.session['otp'] = otp
            request.session['phone_number'] = phone_number
            # Redirect to OTP verification page
            return redirect('otp_verification')
        else:
            messages.error(request, 'This phone number is not registered.')
            return redirect('forget_password')
    else:
        return render(request, 'logininfo/forget_password.html')

# OTP Verification view


def otp_verification(request):
    if request.method == 'POST':
        # Get the OTP entered by the user
        entered_otp = request.POST.get('otp')
        # Get the OTP and phone number from the session
        otp = request.session.get('otp')
        phone_number = request.session.get('phone_number')

        print("Entered OTP:", entered_otp)
        print("Saved OTP:", otp)

        # Check if the entered OTP is correct
        if str(entered_otp) == str(otp):
            # Redirect to reset password page and pass the phone number
            return redirect('reset_password', phone_number=phone_number)
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'logininfo/otp_verification.html')
    else:
        return render(request, 'logininfo/otp_verification.html')
# Helper function to generate and send OTP to the user's phone number


def generate_otp(phone_number):
    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)
    # Send the OTP to the user's phone number using API
    response = requests.post(OTP_API_URL.format(
        phone_number=phone_number, otp=otp))
    # TODO: Handle the response and check if OTP is sent successfully
    print("Generated OTP:", otp)
    return otp

# Reset Password view


def reset_password(request, phone_number):
    if request.method == 'POST':
        # Get the password and confirm password entered by the user
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(
                request, 'Passwords do not match. Please try again.')
            return redirect('reset_password', phone_number=phone_number)

        # Get the user with the given phone number
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            messages.error(
                request, 'User with this phone number does not exist.')
            return redirect('reset_password', phone_number=phone_number)

        # Update the user's password
        user.set_password(password)
        user.save()

        # Redirect to login page
        messages.success(request, 'Password reset successfully.')
        return redirect('show_login_user')
    else:
        return render(request, 'logininfo/reset_password.html', {'phone_number': phone_number})


def check_existing_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            response_data = {'exists': True}
        else:
            response_data = {'exists': False}

        return JsonResponse(response_data)
    else:
        # Handle invalid request method
        return JsonResponse({'error': 'Invalid request method'})


def check_existing_phone(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Check if the phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            response_data = {'exists': True}
        else:
            response_data = {'exists': False}

        return JsonResponse(response_data)
    else:
        # Handle invalid request method
        return JsonResponse({'error': 'Invalid request method'})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        subject = request.POST.get('subject')
        details = request.POST.get('message')

        if details:  # Check if details field is not empty
            feedback_obj = feedback(
                name=name, email=email, mobile=mobile, subject=subject, details=details)
            feedback_obj.save()
            messages.success(
                request, 'Your feedback has been submitted successfully.')
            return redirect('contact')
        else:
            # Display error message if details field is empty
            messages.error(request, 'Please provide a message')

    return render(request, 'contact.html')


def is_valid_nid(nid):
    # NID validation logic goes here
    # You can customize the validation rules based on your requirements

    # NID must be a string of length 10
    if len(nid) != 10:
        return False

    # NID must contain only digits
    if not nid.isdigit():
        return False

    # Additional validation rules...

    # Return True if NID is valid
    return True


@login_required
def proflepage(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            gender = request.POST.get('gender', None)
            profile.user = user
            if gender is not None:
                profile.gender = gender
            # Perform NID validation
            nid = form.cleaned_data['nid']
            if not is_valid_nid(nid):
                form.add_error('nid', 'Invalid NID number')
            else:
                profile.save()
                messages.success(request, 'Your Profile Successfully Updated.')
                # return redirect('dashboard')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiledetails.html', {'form': form})


@login_required
def profilepage(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.instance.user = user
            form.save()
            # Replace 'dashboard' with the appropriate URL or view name
            return redirect('dashboard')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiledetails.html', {'form': form, 'profile': profile})


def faq_page(request):
    categories = Category.objects.all()
    faqs = FAQ.objects.all()
    return render(request, 'faq_page.html', {'categories': categories, 'faqs': faqs})


def terms_and_conditions(request):
    terms = TermsAndConditions.objects.all()
    return render(request, 'termscondition.html', {'terms': terms})


@login_required
def dashboard(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    context = {'user': user, 'profile': profile}

    return render(request, 'dashboard.html', context)


@login_required
def complanints(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  # Assign the current user to the complaint
            complaint.save()
            messages.success(request, 'Complaint submitted successfully.')
            # Replace 'complaint_submitted' with the appropriate URL or view name

        else:
            messages.error(
                request, 'Failed to submit complaint. Please check the form errors.')
    else:
        form = ComplaintForm()

    return render(request, 'complanints.html', {'form': form})


@login_required
def cancelticket(request):
    return render(request, 'cancelticket.html')


def popup_seat_view(request, bus_number=None, coach_number=None, journey_date=None, route_id=None, start_point=None, end_point=None):
    bus = get_object_or_404(Bus, bus_number=bus_number)
    coach = get_object_or_404(Coach, bus=bus, coachnumber=coach_number)
    print('journey_date: ', journey_date)
    print('Start Point: ', start_point)
    print('End Point: ', end_point)

    start_point_route = get_object_or_404(
        BusStop, name__name__iexact=start_point)
    end_point_route = get_object_or_404(BusStop, name__name__iexact=end_point)

    print('Start Point Route: ', start_point_route)
    print('End Point Route: ', end_point_route)

    route_parts = RoutePart.objects.filter(
        start_point=start_point_route, end_point=end_point_route).first()
    print('Route Part Id: ', route_parts.end_point)

    journey_date_coach = coach.journey_dates.first()

    journey_date1 = parse(journey_date).strftime('%Y-%m-%d')
    journey_date_coach = get_object_or_404(
        JourneyDateHistory, journey_date=journey_date1)

    print('Popup date: ', journey_date_coach)

    seat_types = []
    total_rows = 0

    seat_type_1_count = int(bus.seat_type_1) if bus.seat_type_1 else 0
    seat_type_2_count = int(bus.seat_type_2) if bus.seat_type_2 else 0
    seat_type_3_count = int(bus.seat_type_3) if bus.seat_type_3 else 0

    total_columns = 5
    total_rows = int(
        bus.number_or_column) if bus.number_or_column else int(bus.columns)

    # Retrieve booked seats from the Booking model for the specific coach's journey date
    booked_seats = Booking.objects.filter(coach=coach, journey_date=journey_date_coach,
                                          route_part=route_parts, is_booked=True).values_list('seat_number', flat=True)

    print("Booked Seats:", booked_seats)
    print('rote Id: ', route_id)

    # booked_seats = {}
    booked_seats = []
    special_booked_seats = set()
    non_special_booked_seats = set()

    special_route_parts = [
        part for part in route_parts.route.parts.all() if part.is_special_routepart]
    print('special_route_parts: ', special_route_parts)
    print('All Route Parts: ', route_parts.route.parts.all())

    intermediate_route_parts = route_parts.route.intermediate_stops.all()
    intermediate_route_parts_names = [
        stop.name.name for stop in intermediate_route_parts]
    print('intermediate_route_parts: ', intermediate_route_parts)
    print('intermediate_route_parts_names: ', intermediate_route_parts_names)

    # if the seats on the parent route are booked, the seats on the route part will show booked as well

    for special_route_part in special_route_parts:
        special_route_parts_start_point = str(special_route_part.start_point)
        special_route_parts_end_point = str(special_route_part.end_point)
        # special_booked_seats = Booking.objects.filter(
        #     journey_date=journey_date_coach, coach=coach, route_part=special_route_part, is_booked=True
        # ).values_list('seat_number', flat=True)

        # for seat_number in special_booked_seats:
        #     if seat_number not in non_special_booked_seats:
        #         # booked_seats[seat_number] = True
        #         booked_seats.append(seat_number)

    print('special_booked_seats: ', special_booked_seats)
    print("Booked Seats Dictionary:", booked_seats)

    # Fetch all the booked seats for the non-special route parts and add them to the booked_seats dictionary
    # non_special_route_parts = [part for part in route_parts.route.parts.all() if not part.is_special_routepart]

    non_special_route_parts = [part for part in route_parts.route.parts.all()]
    print('non_special_route_parts: ', non_special_route_parts)
    non_special_route_parts_list = [
        non_special_route for non_special_route in non_special_route_parts]
    print('non_special_route_parts_list: ', non_special_route_parts_list)

    route_parts_priority_dict = {}
    priority = 0

    if special_route_parts:
        priority += 1

        # add priority to the start_point of the parent route
        if special_route_parts_start_point not in route_parts_priority_dict:
            route_parts_priority_dict[special_route_parts_start_point] = priority

    # add priority to all the intemediate points on the route
    for intermediate_route_parts_name in intermediate_route_parts_names:
        if intermediate_route_parts_name not in route_parts_priority_dict:
            priority += 1
            route_parts_priority_dict[intermediate_route_parts_name] = priority

    # add priority to the end point of the parent route
    if special_route_parts_end_point not in route_parts_priority_dict:
        priority += 1
        route_parts_priority_dict[special_route_parts_end_point] = priority
    print('route_parts_priority_dict: ', route_parts_priority_dict)

    intermediate_priority_dict = route_parts_priority_dict.copy()
    intermediate_priority_dict_keys = list(intermediate_priority_dict.keys())
    if intermediate_priority_dict:
        if len(intermediate_priority_dict_keys) >= 2:
            del intermediate_priority_dict[intermediate_priority_dict_keys[0]]
            del intermediate_priority_dict[intermediate_priority_dict_keys[-1]]

    print('intermediate_priority_dict_keys: ', intermediate_priority_dict)
    print('route_parts_priority_dict: ', route_parts_priority_dict)

    # for route_part in non_special_route_parts_list:

    #     # the start point and end point are converted to strings to retrieve the priority from dictionary
    #     route_part_start_point = str(route_part.start_point)
    #     route_part_end_point = str(route_part.end_point)
    #     route_part_start_point_priority = route_parts_priority_dict[route_part_start_point]
    #     route_part_end_point_priority = route_parts_priority_dict[route_part_end_point]
    #     print('--------------------------------')

    #     print('route_part_start_point_priority: ', route_part_start_point_priority)
    #     print('route_part_end_point_priority: ', route_part_end_point_priority)

    #     if route_part_start_point and route_part_end_point in route_parts_priority_dict:

    #         for other_route_part in non_special_route_parts_list:
    #             if route_part.start_point == other_route_part.start_point and route_part.end_point == other_route_part.end_point:
    #                 continue
    #             else:
    #                 # take the start point and end point of each of the other route parts to compare
    #                 other_route_part_start_point = str(other_route_part.start_point)
    #                 other_route_part_end_point = str(other_route_part.end_point)

    #                 start_point_priority = (route_parts_priority_dict[other_route_part_start_point])
    #                 end_point_priority = route_parts_priority_dict[other_route_part_end_point]

    #                 print('start_point_priority: ', start_point_priority)
    #                 print('end_point_priority: ', end_point_priority)
    #                 print('----------------------------------------------------------------')

    #                 if start_point_priority < route_part_start_point_priority < end_point_priority and start_point_priority < route_part_end_point_priority < end_point_priority:
    #                     print('priority_sorted: ', route_part)

    # the start point and end point are converted to strings to retrieve the priority from dictionary
    route_part_start_point = str(route_parts.start_point)
    route_part_end_point = str(route_parts.end_point)
    route_part_start_point_priority = route_parts_priority_dict[route_part_start_point]
    route_part_end_point_priority = route_parts_priority_dict[route_part_end_point]
    print('--------------------------------')

    print('route_part_start_point_priority: ', route_part_start_point_priority)
    print('route_part_end_point_priority: ', route_part_end_point_priority)

    if route_part_start_point and route_part_end_point in route_parts_priority_dict:

        for other_route_part in non_special_route_parts_list:
            # take the start point and end point of each of the other route parts to compare
            other_route_part_start_point = str(other_route_part.start_point)
            other_route_part_end_point = str(other_route_part.end_point)

            start_point_priority = route_parts_priority_dict[other_route_part_start_point]
            end_point_priority = route_parts_priority_dict[other_route_part_end_point]

            print('other route part: ', other_route_part)
            print('start_point_priority: ', start_point_priority)
            print('end_point_priority: ', end_point_priority)
            print('route_part_start_point_priority: ',
                  route_part_start_point_priority)
            print('route_part_end_point_priority: ',
                  route_part_end_point_priority)

            if route_parts.start_point == other_route_part.start_point and route_parts.end_point == other_route_part.end_point:

                print('both are equal')

                route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True
                ).values_list('seat_number', flat=True)

                print('route_part_booked_seats: ', route_part_booked_seats)
                print('----------------------------------------------------------------')

                for seat_number in route_part_booked_seats:
                    if seat_number not in booked_seats:
                        booked_seats.append(seat_number)

            elif start_point_priority > route_part_start_point_priority and start_point_priority >= route_part_end_point_priority \
                    and end_point_priority > route_part_end_point_priority:

                print('Second if')
                route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True
                ).values_list('seat_number', flat=True)

                print('second route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            elif start_point_priority < route_part_start_point_priority and end_point_priority <= route_part_start_point_priority \
                    and end_point_priority < route_part_end_point_priority:

                print('Third if')
                route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True
                ).values_list('seat_number', flat=True)

                print('third route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            # inside the parent route
            elif (start_point_priority <= route_part_start_point_priority and end_point_priority >= route_part_end_point_priority) \
                    or route_part_start_point_priority < start_point_priority < route_part_end_point_priority \
                    or route_part_start_point_priority < end_point_priority < route_part_end_point_priority:

                other_route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=other_route_part, is_booked=True
                ).values_list('seat_number', flat=True)
                print('other_route_part_booked_seats: ',
                      other_route_part_booked_seats)
                print('----------------------------------------------------------------')

                for seat_number in other_route_part_booked_seats:
                    if seat_number not in booked_seats:
                        booked_seats.append(seat_number)

            else:
                # take the start point and end point of each of the other route parts to compare

                # print('start_point_priority: ', start_point_priority)
                # print('end_point_priority: ', end_point_priority)
                # print('route_part_start_point_priority: ', route_part_start_point_priority)
                # print('route_part_end_point_priority: ', route_part_end_point_priority)
                # print('----------------------------------------------------------------')
                print('nothing matched!!')

                # if start_point_priority < route_part_start_point_priority < end_point_priority and start_point_priority < route_part_end_point_priority < end_point_priority:

    # print('route part name: ', route_part.start_point)

    # for non_special_route_part in non_special_route_parts:
    #     non_special_booked_seats.update(
    #         Booking.objects.filter(
    #             journey_date=journey_date_coach, coach=coach, route_part=non_special_route_part, is_booked=True
    #         ).values_list('seat_number', flat=True)
    #     )

    # for seat_number in special_booked_seats:
    #     # booked_seats[seat_number] = True
    #     booked_seats.append(seat_number)

    # for seat_number in non_special_booked_seats:
    #     # booked_seats[seat_number] = False
    #     booked_seats.append(seat_number)

    print("Booked Seats Dictionary1:", booked_seats)

    # Now, the special_booked_seats set contains all booked seats for both special and non-special route parts

    route = Route.objects.get(id=route_id)
    print('route_part: ', route.parts.all())
    # print('Coach routes: ', coach_routes)
    # for route in coach_routes:
    #     print('rouete: ', route.id)

    # print('boarding: ', route_id)

    if route_id:
        route = Route.objects.get(id=route_id)
        boarding_points = route.boarding_points.all()
        print('boarding_points: ', boarding_points)

    rows_seat_type_1 = []
    rows_seat_type_2 = []
    rows_seat_type_3 = []
    rows_seat_type_1_len = 0
    rows_seat_type_2_len = 0
    rows_seat_type_3_len = 0
    rows_type_1, rows_type_2, rows_type_3 = generate_rows(
        seat_type_1_count, seat_type_2_count, seat_type_3_count)
    rows_type_index_1 = [(index, seat_row)
                         for index, seat_row in enumerate(rows_type_1)]
    rows_type_index_2 = [(index, seat_row)
                         for index, seat_row in enumerate(rows_type_2)]
    rows_type_index_3 = [(index, seat_row)
                         for index, seat_row in enumerate(rows_type_3)]
    # print('rows_type_1: ', rows_type_1 )
    # print('rows_type_2: ', rows_type_2)
    # print('rows_type_3: ', rows_type_3)
    print('rows_type_2 len: ', len(rows_type_2) - 1)
    print('rows_type_index_1: ', rows_type_index_1)
    print('rows_type_index_2: ', rows_type_index_2)
    print('rows_type_index_3: ', rows_type_index_3)

    print('seat_type_1_count: ', seat_type_1_count)
    print('seat_type_2_count: ', seat_type_2_count)
    print('seat_type_3_count: ', seat_type_3_count)

    print('len(rows_type_index_2) - 1,: ', len(rows_type_index_2) - 1,)

    if seat_type_1_count > 0:
        seat_type_1 = '1:1'
        seat_types.append({
            'type': seat_type_1,
            # 'seats': generate_seats(seat_type_1, seat_type_1_count, total_columns, booked_seats),
            'rows': rows_type_index_1,
            'total_seats': seat_type_1_count * total_columns,
        })

    if seat_type_2_count > 0:
        seat_type_2 = '1:2'
        seat_types.append({
            'type': seat_type_2,
            # 'seats': generate_seats(seat_type_2, seat_type_2_count, total_columns, booked_seats),
            'rows': rows_type_index_2,
            'type_2_row_len': len(rows_type_index_2) - 1,
            'total_seats': seat_type_2_count,
        })

    if seat_type_3_count > 0:
        seat_type_3 = '2:2'
        seat_types.append({
            'type': seat_type_3,
            # 'seats': generate_seats(seat_type_3, seat_type_3_count, total_columns, booked_seats),
            'rows': rows_type_index_3,
            'type_3_row_len': len(rows_type_index_3) - 1,
            'total_seats': seat_type_3_count * total_columns,
        })

    if rows_type_1 and not rows_type_2 and not rows_type_3:
        seat_type_1 = '1:1'
        rows_seat_type_1 = rows_type_index_1
        rows_seat_type_1_len = len(rows_type_1) - 1
        rows_seat_type_2_len = 0
        rows_seat_type_3_len = 0

    elif rows_type_2 and not rows_type_1 and not rows_type_3:
        seat_type_2 = '1:2'
        rows_seat_type_2 = rows_type_index_2
        rows_seat_type_2_len = len(rows_type_2) - 1
        rows_seat_type_1_len = 0
        rows_seat_type_3_len = 0

    elif rows_type_3 and not rows_type_1 and not rows_type_2:
        seat_type_3 = '2:2'
        rows_seat_type_3 = rows_type_index_3
        rows_seat_type_3_len = len(rows_type_3) - 1
        rows_seat_type_1_len = 0
        rows_seat_type_2_len = 0

    total_rows = seat_type_1_count + seat_type_2_count + seat_type_3_count
    print('rows_seat_type_1: ', seat_type_1_count)
    print('rows_seat_type_2: ', seat_type_2_count)
    print('rows_seat_type_3: ', rows_seat_type_3)

    if rows_seat_type_1:
        print('Found rows_seat_type_1')
    else:
        print('not Found rows_seat_type_1')
    extra_seat = bus.extra_seat
    print('extra_seat: ', extra_seat)
    print('seat_types: ', seat_types)

    remaining_rows = total_rows - seat_type_1_count - \
        seat_type_2_count - seat_type_3_count

    # if remaining_rows > 0:
    #     mixed_seats = generate_seats(
    #         'mixed', remaining_rows, total_columns, booked_seats)
    # else:
    #     mixed_seats = []
    #     print('Mixed hit in popup')

    #     seat_types.append({
    #         'type': 'mixed',
    #         'seats': mixed_seats,
    #         # 'rows': generate_rows(remaining_rows),
    #         'rows': generate_mixed_seats(bus, total_rows, total_columns),
    #         'total_seats': remaining_rows * total_columns,
    #     })

    context = {
        'seat_types': seat_types,
        'bus': bus,
        'selected_bus': bus,
        'total_rows': total_rows,
        'coach': coach,
        'journey_date_coach': journey_date_coach,
        'boarding_points': boarding_points,
        'booked_seats': json.dumps(list(booked_seats)),
        'route_id': route_id,
        'route_part_id': route_parts.id,
        'seat_type_1_count': seat_type_1_count,
        'seat_type_2_count': seat_type_2_count,
        'seat_type_3_count': seat_type_3_count,
        # 'seat_type_1': seat_type_1,
        # 'seat_type_2': seat_type_2,
        # 'seat_type_3': seat_type_3,
        'rows_seat_type_1': rows_seat_type_1,
        'rows_seat_type_2': rows_seat_type_2,
        'rows_seat_type_3': rows_seat_type_3,
        'rows_seat_type_1_len': rows_seat_type_1_len,
        'rows_seat_type_2_len': rows_seat_type_2_len,
        'rows_seat_type_3_len': rows_seat_type_3_len,
        'extra_seat': extra_seat,
        'total_rows': total_rows
    }

    return render(request, 'popupseat.html', context)


def generate_rows(seat_type_1, seat_type_2, seat_type_3):
    rows_type_1 = []
    rows_type_2 = []
    rows_type_3 = []
    row_1 = 0
    row_2 = 0
    row_3 = 0

    if seat_type_1 > 0 and seat_type_2 == 0 and seat_type_3 == 0:
        for row_1 in range(int(seat_type_1)):
            rows_type_1.append(chr(65 + (row_1 % 11)))

    elif seat_type_1 == 0 and seat_type_2 > 0 and seat_type_3 == 0:
        for row_2 in range(int(seat_type_2)):
            rows_type_2.append(chr(65 + (row_2 % 11)))

    elif seat_type_1 == 0 and seat_type_2 == 0 and seat_type_3 > 0:
        for row_3 in range(int(seat_type_3)):
            rows_type_3.append(chr(65 + (row_3 % 11)))

    else:
        if seat_type_1 > 0:
            for row_1 in range(int(seat_type_1)):
                rows_type_1.append(chr(65 + (row_1 % 11)))

        if seat_type_2 > 0:
            for row_2 in range(row_1 + 1, int(seat_type_2) + row_1 + 1):
                rows_type_2.append(chr(65 + (row_2 % 11)))

        if seat_type_3 > 0:
            for row_3 in range(row_2 + 1, int(seat_type_3) + row_2 + 1):
                rows_type_3.append(chr(65 + (row_3 % 11)))

        # if seat_type_1 > 0:
        #     for row_1 in range(int(seat_type_1)):
        #         rows_type_1.append(chr(65 + (row_1 % 11)))
        # if row_1 > 0:
        #     if seat_type_2 > 0:
        #         for row_2 in range(row_1 + 1, int(seat_type_2) + row_1 + 1):
        #             rows_type_2.append(chr(65 + (row_2 % 11)))

        # else:
        #     if seat_type_2 > 0:
        #        for row_2 in range(int(seat_type_2)):
        #             rows_type_2.append(chr(65 + (row_2 % 11)))

        # if row_2 > 0:
        #     if seat_type_3 > 0:
        #         for row_3 in range(row_2 + 1, int(seat_type_3) + row_2 + 1):
        #             rows_type_3.append(chr(65 + (row_3 % 11)))

        # else:
        #     if seat_type_3 > 0:
        #         for row_3 in range(int(seat_type_3)):
        #             rows_type_3.append(chr(65 + (row_3 % 11)))

    return rows_type_1, rows_type_2, rows_type_3


# def generate_seats(seat_type, quantity, columns, booked_seats):
#     seats = []
#     if seat_type == '1:1':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for _ in range(columns):
#                 seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                 is_booked = seat in booked_seats
#                 row.append({'seat': seat, 'is_booked': is_booked})
#                 seat_number += 2
#             seats.append(row)
#     elif seat_type == '1:2':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for i in range(columns):
#                 if i % 3 == 0:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#                 elif i % 3 == 1:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 2
#                 else:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 2
#             seats.append(row)
#     elif seat_type == '2:2':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for i in range(columns):
#                 if i % 3 == 0 or i % 3 == 1:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#                 else:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#             seats.append(row)
#     else:
#         for _ in range(int(quantity)):
#             row = [{'seat': 'None Seats', 'is_booked': False}] * columns
#             seats.append(row)
#     return seats


# def generate_mixed_seats(bus, quantity, columns):
#     seats = []
#     print("its a hit!!!")
#     for row_num in range(int(quantity)):
#         row = []
#         for i in range(columns):
#             if i % 3 == 0:
#                 seat = Seat(bus=bus, seat_type='seat_type_1', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#             elif i % 3 == 1:
#                 seat = Seat(bus=bus, seat_type='seat_type_2', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#             else:
#                 seat = Seat(bus=bus, seat_type='seat_type_3', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#         seats.append(row)
#     bus.save()
#     return seats


# def generate_rows(quantity):
#     rows = []
#     for i in range(int(quantity)):
#         rows.append(chr(65 + (i % 10)))
#     return rows


# def generate_seats(seat_type, quantity, columns, booked_seats):
#     seats = []
#     if seat_type == '1:1':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for _ in range(columns):
#                 seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                 is_booked = seat in booked_seats
#                 row.append({'seat': seat, 'is_booked': is_booked})
#                 seat_number += 2
#             seats.append(row)
#     elif seat_type == '1:2':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for i in range(columns):
#                 if i % 3 == 0:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#                 elif i % 3 == 1:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 2
#                 else:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 2
#             seats.append(row)
#     elif seat_type == '2:2':
#         seat_number = 1
#         for _ in range(int(quantity)):
#             row = []
#             for i in range(columns):
#                 if i % 3 == 0 or i % 3 == 1:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#                 else:
#                     seat = '{}{}'.format(chr(65 + (_ % 10)), seat_number)
#                     is_booked = seat in booked_seats
#                     row.append({'seat': seat, 'is_booked': is_booked})
#                     seat_number += 1
#             seats.append(row)
#     else:
#         for _ in range(int(quantity)):
#             row = [{'seat': 'None Seats', 'is_booked': False}] * columns
#             seats.append(row)
#     return seats


# def generate_mixed_seats(bus, quantity, columns):
#     seats = []
#     for row_num in range(int(quantity)):
#         row = []
#         for i in range(columns):
#             if i % 3 == 0:
#                 seat = Seat(bus=bus, seat_type='seat_type_1', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#             elif i % 3 == 1:
#                 seat = Seat(bus=bus, seat_type='seat_type_2', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#             else:
#                 seat = Seat(bus=bus, seat_type='seat_type_3', row_number=chr(
#                     65 + (row_num % 10)), seat_number=str(bus.total_seats))
#                 row.append(seat)
#                 bus.total_seats += 1
#         seats.append(row)
#     bus.save()
#     return seats


def generate_ticket_pdf(journey_date, coach_number, seat_number, price, pnr, user_name):
    buffer = BytesIO()

    # Create a Canvas object and draw on it
    c = canvas.Canvas(buffer, pagesize=A4)

    # PDF content starts

    c.translate(inch, inch)
    c.drawImage('bus/static/img/bus_logo1.jpg', -0.5*inch, 9*inch)
    c.setStrokeColorRGB(0.75, 0.75, 0.75)

    c.drawImage('bus/static/img/logo5.png', 4.1 *
                inch, 9.3*inch, width=200, height=50)

    c.setLineWidth(60)
    c.line(-1*inch, 8.5*inch, 10*inch, 8.5*inch)

    # Route heading
    c.setFont('Helvetica', 20)
    c.drawString(-20, 605, 'Dhaka to Chottogram')
    c.drawImage('bus/static/img/clock5.png', 395, 600, mask='auto')
    c.setFont('Helvetica', 12)

    # Journey date
    c.drawString(425, 615, journey_date)
    c.drawString(425, 600, '9.00 AM')

    # Ticket info starts
    c.setLineWidth(2)
    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.rect(-1.3*inch, 7*inch, 10*inch, 0.8*inch, fill=1)

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)
    c.drawString(-30, 540, 'Passenger Name')

    c.setFillColorRGB(0.239, 0.294, 0.49)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(-30, 525, user_name)

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)
    c.drawString(140, 540, 'Coach #')

    c.setFillColorRGB(0.239, 0.294, 0.49)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(140, 525, coach_number)

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)
    c.drawString(230, 540, 'Seat #')

    c.setFillColorRGB(0.239, 0.294, 0.49)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(230, 525, seat_number)

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)
    c.drawString(340, 540, 'PNR')

    c.setFillColorRGB(0.239, 0.294, 0.49)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(340, 525, pnr)

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)
    c.drawString(420, 540, 'Total Fare')

    c.setFillColorRGB(0.239, 0.294, 0.49)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(420, 525, 'BDT ' + price)
    # Ticket info ends

    # Boarding Point
    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 15)

    c.setFillColorRGB(0.133, 0.349, 0.094)
    c.drawString(-20, 460, 'Boarding Point')

    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)

    # Boarding Point starts
    max_width = 200  # Maximum width of the text before wrapping

    # Boarding Point Counter Address
    long_text = 'Jean Baptiste Point du Sable Lake Shore Drive” located in Chicago, Illinois. Sable Lake Shore Drive” located in Chicago, Illinois'

    # Create a style for the Paragraph
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'Helvetica'
    style.fontSize = 12

    # Create a Paragraph with the long text and apply the style
    paragraph = Paragraph(long_text, style)

    # Wrap the text within the given max_width
    boarding_destination_y = 440
    paragraph.wrap(max_width, boarding_destination_y)

    # Get the height of the wrapped paragraph
    paragraph_height = paragraph.height

    adjusted_y = boarding_destination_y - paragraph_height

    # Draw the Paragraph on the canvas
    paragraph.drawOn(c, -20, adjusted_y)

    c.setFillColorRGB(0.133, 0.349, 0.094)
    c.setFont('Helvetica', 15)
    c.drawString(-20, adjusted_y-20, 'Dhaka')

    # Boarding Point ends

    # Destination starts
    c.setFont('Helvetica', 15)
    c.setFillColorRGB(0.922, 0.337, 0.337)
    c.drawString(270, 460, 'Destination')

    destination_address = 'Jean Baptiste Point du Sable Lake Shore Drive” located in Chicago, Illinois. Sable Lake Shore Drive” located in Chicago, Illinois'
    c.setFillColorRGB(0, 0, 0)
    c.setFont('Helvetica', 12)

    # Create a style for the Paragraph
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'Helvetica'
    style.fontSize = 12

    # Create a Paragraph with the long text and apply the style
    paragraph = Paragraph(destination_address, style)

    # Wrap the text within the given max_width
    paragraph.wrap(max_width, boarding_destination_y)

    # Get the height of the wrapped paragraph
    paragraph_height = paragraph.height

    adjusted_y1 = boarding_destination_y - paragraph_height

    # Draw the Paragraph on the canvas
    paragraph.drawOn(c, 270, adjusted_y1)

    c.setFillColorRGB(0.922, 0.337, 0.337)
    c.setFont('Helvetica', 15)
    c.drawString(270, adjusted_y1-20, 'Chottogram')
    # Destination ends

    print('adjusted_y1: ', adjusted_y1)
    print('adjusted_y: ', adjusted_y)

    # y coordinate of location image
    if adjusted_y1 < adjusted_y:
        location_y = adjusted_y1 - 70

    elif adjusted_y1 > adjusted_y:
        location_y = adjusted_y1 - 70

    elif adjusted_y1 == adjusted_y:
        location_y = adjusted_y - 70

    c.drawImage('bus/static/img/departure_location.png', 20, location_y)
    c.drawImage('bus/static/img/arrival_loation.png', 390, location_y)

    c.setStrokeColorRGB(0.75, 0.75, 0.75)
    c.setLineWidth(5)
    c.line(30, location_y-5, 400, location_y-5)

    # Departure time starts
    departure_arrival_time_y = location_y - 30
    departure_time_y = departure_arrival_time_y - 20

    c.setFillColorRGB(0.133, 0.349, 0.094)
    c.drawString(0, departure_arrival_time_y, 'Departure Time:')

    bold_font_name = 'Helvetica-Bold'
    c.setFont(bold_font_name, 15)
    c.setFillColorRGB(0.133, 0.349, 0.094)
    c.drawString(0, departure_time_y, '9:30 AM')
    # Departure time ends

    # Arrival time starts
    c.setFont('Helvetica', 15)
    c.setFillColorRGB(0.922, 0.337, 0.337)
    c.drawString(370, departure_arrival_time_y, 'Arrival Time:')

    bold_font_name = 'Helvetica-Bold'
    c.setFont(bold_font_name, 15)
    c.drawString(370, departure_time_y, '5:30 PM')
    # Arrival time ends

    # Terms and Condition
    terms_heading_y = departure_time_y - 25
    c.setFont('Helvetica-Bold', 15)
    c.setFillColorRGB(0, 0, 0)
    bullet_x = -20  # X-coordinate of the bullet point
    bullet_y = terms_heading_y - 25  # Y-coordinate of the bullet point
    c.drawString(bullet_x + 15, terms_heading_y - 8, 'Terms and Conditions')
    print('bullet_y: ', bullet_y)

    # Custom bullet point size
    bullet_radius = 2.5

    # Draw the circle bullet point
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(0.5)  # Adjust the line width of the circle
    c.circle(bullet_x + bullet_radius, bullet_y -
             bullet_radius, bullet_radius, fill=1)
    max_width_terms = 500

    # Draw the text after the bullet point
    text1 = "Change of bus: In case the bus operator changes the type of bus due tosome reason, redBus will refund the differential amount to the customerupon being intimated by the customers in 24 hours of the journey"

    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0, 0, 0)

    # Create a style for the Paragraph
    styles_terms = getSampleStyleSheet()
    style_terms = styles_terms['Normal']
    style_terms.fontName = 'Helvetica'
    style_terms.fontSize = 9

    # Create a Paragraph with the long text and apply the style
    paragraph_terms = Paragraph(text1, style_terms)

    # Wrap the text within the given max_width
    paragraph_terms.wrap(max_width_terms, bullet_y)

    # Get the height of the wrapped paragraph
    paragraph_terms_height = paragraph_terms.height

    adjusted_terms_y = bullet_y - paragraph_terms_height

    # Draw the Paragraph on the canvas
    paragraph_terms.drawOn(c, 0, adjusted_terms_y + 3)
    # c.drawString(bullet_x + 15, bullet_y - 8, text1)  # Adjust the x-coordinate for the text position

    # PDF content ends
    c.showPage()
    c.save()

    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content


def booking(request, bus_number, coach_number, journey_date, route_id, route_part_id):
    bus = get_object_or_404(Bus, bus_number=bus_number)
    coach = get_object_or_404(Coach, bus=bus, coachnumber=coach_number)
    coach_bus = bus

    print('Booking route id: ', route_part_id)

    journey_date_str = datetime.strptime(journey_date, '%Y-%m-%d').date()
    journey_dates = JourneyDateHistory.objects.filter(
        journey_date=journey_date_str).first()

    selected_seat = request.GET.get('seat', '').strip()
    selected_price = request.GET.get('price', '')
    tax = Tax.objects.filter(status=1).first()
    tax_value = float(tax.tax_value)
    tax_name = tax.tax_name

    try:
        selected_price = format(float(selected_price), '.2f')
        selected_price = float(selected_price)
        tax_amount = math.ceil(selected_price * (tax_value / 100))
        total_payable_amount = selected_price + tax_amount

        tax_amount_str = format(tax_amount, '.2f')
        total_payable_amount_str = format(total_payable_amount, '.2f')

        print(type(selected_price))

    except:
        selected_price = ''
        # tax_amount = ''
        tax_amount_str = ''
        total_payable_amount_str = ''
    selected_seats_list = selected_seat.split() if selected_seat else []

    print('selected_seat: ', selected_seat)
    print('selected_price: ', selected_price)

    route_part = RoutePart.objects.get(id=route_part_id)

    selected_boarding_point_id = request.GET.get('boarding_point', '')

    if selected_boarding_point_id:
        try:
            selected_boarding_point = BoardingPoint.objects.get(
                id=selected_boarding_point_id)
        except BoardingPoint.DoesNotExist:
            selected_boarding_point = None
    else:
        selected_boarding_point = None

    # Generate an 8-digit random PNR
    pnr = str(random.randint(10000000, 99999999))
    print("pnr:", pnr)

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            email = user.email
        else:
            email = request.POST.get('email', '')
            if email == None:
                messages.error(request, 'Please enter your email address')
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None

        selected_seat = request.POST.get('seat_number', '')
        selected_price = request.POST.get('price', '')
        selected_price = float(selected_price)

        tax_amount = math.ceil(selected_price * (tax_value / 100))
        total_payable_amount = selected_price + tax_amount

        tax_amount_str = format(tax_amount, '.2f')
        total_payable_amount_str = format(total_payable_amount, '.2f')

        print("Seat Number:", selected_seat)
        print('total booking price after post: ', type(selected_price))

        # Convert selected_price to an integer
        try:
            price = int(selected_price) if selected_price else 0
        except (ValueError, TypeError):
            price = 0
        print('price of booking: ', price)
        if selected_seat and price > 0:
            if Booking.objects.filter(coach=coach, seat_number=selected_seat, is_booked=True, journey_date=journey_dates).exists():
                messages.error(request, 'Seat already booked.')
            else:
                # Generate an 8-digit random PNR
                pnr = str(random.randint(10000000, 99999999))
                booking = Booking.objects.create(
                    user=user,
                    coach=coach,
                    seat_number=selected_seat,
                    route_part=route_part,
                    price=price,
                    is_booked=True,
                    journey_date=journey_dates,
                    pnr=pnr,  # Assign the generated PNR to the booking
                    route_id=route_id
                )
                messages.success(request, 'Ticket booking successful.')

                # subject = 'welcome to our bus webste'
                # message = 'Hi thank you for registering in our bus website.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['ajayghosh28@gmail.com' ]
                # send_mail( subject, message, email_from, recipient_list )

                coach_number = coach.coachnumber
                booking_date = booking.journey_date
                booking_seat = booking.seat_number
                ticket_price = booking.price
                ticket_pnr = booking.pnr
                user_name = email

                pdf_content = generate_ticket_pdf(str(booking_date), str(coach_number), str(
                    booking_seat), str(ticket_price), str(ticket_pnr), str(user_name))
                pdf_file = ContentFile(pdf_content)

                template_name = 'email_booking.html'
                content = render_to_string(template_name)
                # html_content = content

                # Create the EmailTemplate with the updated plain text and HTML content
                # EmailTemplate.objects.create(
                #     name=template_name,
                #     subject='Booking Successful',
                #     content=content,
                #     html_content=html_content,
                # )
                context = {
                    'user': user.first_name,
                    'coach_number': coach_number,
                    'journey_date': booking_date,
                    'seat_number': booking_seat,
                    'price': ticket_price,
                    'pnr': ticket_pnr,
                    'route_part_id': route_part_id,
                    'tax_amount_str': tax_amount_str,
                    'total_payable_amount_str': total_payable_amount_str
                }

                html_content = render_to_string(template_name, context)

                mail.send(
                    [email],
                    settings.EMAIL_HOST_USER,
                    # subject='<strong>Hello from Django Post Office</strong>',
                    subject='Booking Successful',
                    # message=content,
                    html_message=html_content,
                    # template=template_name,
                    # message='This is the email content.',
                    # context=context,
                    attachments={'ticket.pdf': pdf_file},
                    priority='now'
                )

                print('Email: ', email)
                # html_message = render_to_string()
                # email_from = settings.EMAIL_HOST_USER

        else:
            messages.error(request, 'Invalid seat number or price.')

    booked_seats = Booking.objects.filter(
        coach=coach).values_list('seat_number', flat=True)

    context = {
        'bus': bus,
        'coach': coach,
        'coach_bus': coach_bus,
        'selected_seat': selected_seat,
        'selected_price': selected_price,
        'booked_seats': booked_seats,
        'journey_date': journey_dates,
        'route_id': route_id,
        'route_part': route_part,
        'route_part_id': route_part_id,
        'selected_boarding_point': selected_boarding_point,
        'pnr': pnr,
        # Pass the generated PNR to the template
        'selected_seats_list': selected_seats_list,
        'tax_amount': tax_amount_str,
        'total_payable_amount_str': total_payable_amount_str
    }

    return render(request, 'ticketbooking.html', context)


def search_booking(request):
    if request.method == 'POST':
        # Debugging: Print the form data to the console
        print("Form data received:", request.POST)
        pnr = request.POST.get('pnr_number')
        identifier = request.POST.get('mobile')
        try:
            # Search for the booking based on the provided PNR and user's phone number or email
            booking = Booking.objects.get(
                Q(pnr=pnr),
                Q(user__phone_number=identifier) | Q(user__email=identifier)
            )
            # Debugging: Print the found booking
            print("Booking found:", booking)
            # Check if a CancelTicket object already exists for this booking
            cancel_ticket = CancelTicket.objects.filter(
                booking=booking).first()
            if cancel_ticket:
                # Get the status of the existing cancel request
                request_status = cancel_ticket.status
                messages.success(
                    request, 'Your cancel request status has been fetched.')
                return render(request, 'cancel_request_status.html', {'request_status': request_status})
            if 'cancel_request' in request.POST:
                # Create a new CancelTicket object and set the status to 'Pending'
                cancel_ticket = CancelTicket.objects.create(
                    booking=booking, status='Pending', cancel_fee=50)
                request_status = 'Pending'
                messages.success(
                    request, 'Thank you for being with us. Your cancel request has been received.')
                # Pass the request_status to the template context
                return render(request, 'cancel_request_status.html', {'request_status': request_status})
            return render(request, 'ticket_cancel.html', {'booking': booking, 'identifier': identifier})
        except Booking.DoesNotExist:
            messages.error(
                request, 'No booking found with the provided details.')
    return render(request, 'cancelticket.html')


def insurance(request):
    return render(request, 'insurance.html')


def insurance_term(request):
    return render(request, 'term_condition_insurance.html')


def my_ticket_list(request):
    # Get a list of bookings for the current user (replace with your logic)
    user = request.user  # Assuming you're using Django's built-in authentication
    bookings = Booking.objects.filter(user=user)
    # Create an empty list to store booking details
    booking_details = []
    # Iterate through each booking in the QuerySet
    for booking in bookings:
        # Check if there is a corresponding cancellation request
        cancel_ticket = CancelTicket.objects.filter(booking=booking).first()
        current_date = timezone.now().date()
        journey_date = booking.journey_date.journey_date
        start_point = booking.route_part.start_point.name
        end_point = booking.route_part.end_point.name

        # Calculate the booking status based on your conditions
        if not booking.is_paid and booking.is_booked and journey_date >= current_date:
            status = 'Booked'
        elif journey_date < current_date:
            status = 'Expired'
        elif booking.is_paid:
            status = 'Paid'
        elif booking.is_booked is False:
            status = 'Cancelled'
        else:
            status = 'Active'

        # Create a dictionary for each booking's details
        booking_detail = {
            # 'status': cancel_ticket.status if cancel_ticket else 'Not Cancelled',
            'booking': booking,
            'status': status,
            'total_fare': booking.price,
            'bus_type': booking.coach.bus.bus_type,
            'booking_date': booking.journey_date,
            # You may need to adjust this based on your model structure
            'expire_time': booking.coach.depraturetime,
            'journey_date': journey_date,
            'start_point': start_point,
            'end_point': end_point
        }
        # Add the booking_detail dictionary to the list
        booking_details.append(booking_detail)
    context = {
        'booking_details': booking_details,
    }
    return render(request, 'myticket.html', context)


def my_ticket_details(request, booking_id):
    user = request.user
    if user.is_authenticated:
        booking = Booking.objects.filter(id=booking_id, user=user).first()
        cancel_ticket = CancelTicket.objects.filter(booking=booking).first()
        current_date = timezone.now().date()
        journey_date = booking.journey_date.journey_date
        start_point = booking.route_part.start_point.name
        end_point = booking.route_part.end_point.name
        coach = booking.coach
        coach_number = coach.coachnumber
        departure_time = coach.depraturetime
        seat_number = booking.seat_number
        user_name = f"{user.first_name} {user.last_name}"
        phone_number = user.phone_number
        seat_fare = booking.price
        # Calculate the booking status based on your conditions
        if not booking.is_paid and booking.is_booked and journey_date >= current_date:
            status = 'Booked'
        elif journey_date < current_date:
            status = 'Expired'
        elif booking.is_paid:
            status = 'Paid'
        elif booking.is_booked is False:
            status = 'Cancelled'
        else:
            status = 'Active'
        context = {
            'booking': booking,
            'cancel_ticket': cancel_ticket,
            'current_date': current_date,
            'journey_date': journey_date,
            'start_point': start_point,
            'end_point': end_point,
            'coach': coach,
            'coach_number': coach_number,
            'departure_time': departure_time,
            'seat_number': seat_number,
            'user_name': user_name,
            'phone_number': phone_number,
            'seat_fare': seat_fare,
            'status': status,  # Include the status in the context
        }
        return render(request, 'my_ticket_details.html', context)


def pay_now(request, booking_id):
    # Retrieve the booking based on the booking_id
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        # Get the payment amount from the form
        payment_amount = request.POST.get('payment_amount')
        # Create a payment record
        payment = Payment.objects.create(
            booking=booking,
            payment_type=booking.payment_method,  # Replace with your payment method logic
            amount_paid=payment_amount,
            created_by=request.user,  # Assuming you have user authentication
        )
        # Update the payment status of the booking
        booking.update_payment_status()
        # Show a success message
        messages.success(request, 'Payment successful!')
        # Redirect to a success page or any other page
        return redirect('success_page')  # Replace with your success page URL
    # Render the payment form
    return render(request, 'payment_form.html', {'booking': booking})
