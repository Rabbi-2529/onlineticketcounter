from .models import Counter, BusStop, Route
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Customers, Staffs, Bus, CustomUser
from django.db.models import Sum
# from bus.forms import AddCustomerForm, EditCustomerForm
from bus.models import CustomUser, Staffs, Customers, Visitor
from django.shortcuts import render, redirect
from django.contrib import messages
from bus.models import Counter, District, FAQ, Category, Bus, Seat, Route, Coach, feedback, BoardingPoint, JourneyDateHistory, Click, Division, District, Upazila, Union, Facility, BusStop, RoutePart, Thana, StaffType, Vehicle, Tax, PaymentMethod, Staffs, BusFitness, PermissionCategory, CustomPermission, PopupDuration, Refund, Payment, Company
from .forms import BusRegistrationForm, BookingForm
from django.utils.decorators import method_decorator
from datetime import timedelta
from datetime import datetime
from datetime import date
from django.db.models import Q
from django.core import serializers
import json
from django.db import IntegrityError
from bus.models import profile_picture_upload
from django.conf import settings
from django.core.mail import send_mail
from post_office import mail
from django.db.models import Count, Case, When, Value, IntegerField
from django.contrib.auth.decorators import login_required
from dateutil.parser import parse
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Staffs, Users
# from .forms import CreateUserForm  # Import your form class
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import uuid
from django.views import View
from .models import Bus, Coach
from dateutil.parser import parse
import datetime
import json
import os
import math
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
from bus.models import CustomUser, TicketBooking, Coach, Route, PropularRoutes, Counter, District, Category, FAQ, TermsAndConditions, Profile, Bus, Seat, Booking, JourneyDateHistory, CancelTicket, BusStop, RoutePart
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
from django.contrib.auth.decorators import login_required
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
from django.core.validators import validate_email
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
from django.contrib.auth import update_session_auth_hash
from random import randint
from django.contrib.auth.decorators import user_passes_test
from django.utils import translation
from django.http import FileResponse
from decimal import Decimal, DecimalException
from django.contrib.auth import get_user

from django.utils.decorators import method_decorator
from .decorators import user_type_required


@user_type_required(user_types=[0])
@login_required
def root_home(request):

    return render(request, "root_template/home_content.html")


@login_required
@user_type_required(user_types=[0])
def create_company(request):
    # Check if the user is a root user (user_type=0)
    if request.user.user_type == 0:
        if request.method == 'POST':
            try:
                # Get company and super admin user information from the request
                company_name = request.POST.get('company_name')
                superadmin_name = request.POST.get('superadmin_name')
                superadmin_email = request.POST.get('superadmin_email')
                superadmin_mobile = request.POST.get('superadmin_mobile')
                superadmin_password = request.POST.get('superadmin_password')
                superadmin_address = request.POST.get('superadmin_address')
                # Assuming you have an image field
                superadmin_image = request.FILES.get('superadmin_image')

                # Create a new company with the given name and associate it with the super admin user
                company, created_at = Company.objects.get_or_create(
                    name=company_name, user_name=superadmin_name, email=superadmin_email, root_user=request.user)

                # Create a new super admin user (user_type 2 for Staff)
                user = CustomUser.objects.create_user(
                    username=superadmin_email,  # You can use email as the username
                    email=superadmin_email,
                    password=superadmin_password,
                    user_type=1,  # Staff (super admin)
                    phone_number=superadmin_mobile,
                    address=superadmin_address,
                    profile_picture=superadmin_image,
                    company=company
                )

                # Split the user's name if a space exists, otherwise use a default value
                superadmin_name_parts = superadmin_name.split(' ')
                if len(superadmin_name_parts) >= 2:
                    user.first_name, user.last_name = superadmin_name_parts
                else:
                    user.first_name = superadmin_name
                    user.last_name = ""

                user.save()

                messages.success(
                    request, 'Company created successfully!')
                return redirect('create_company')

            except Exception as e:
                error_message = f"Error creating company: {str(e)}"
                messages.error(request, error_message)
                print(error_message)

        # Render the form for company creation (GET request)
        return render(request, 'root_template/create_company.html')

    else:
        messages.error(request, 'Only root users can create companies.')
        return redirect('root_home')


def company_list(request):
    companies = Company.objects.all()
    context = {'companies': companies}
    return render(request, 'root_template/company_list.html', context)


def staff_type_list(request):
    staff_types = StaffType.objects.all()
    return render(request, 'root_template/staff_type_list.html', {'staff_types': staff_types})


def create_staff_type(request):
    staff_type_choices = StaffType.STAFF_TYPE_CHOICES

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        try:
            # Check if the staff type with the given name already exists
            StaffType.objects.get(name=name)
            error_message = f'Staff type "{name}" already exists.'
            return render(request, 'root_template/create_staff_type.html', {'staff_type_choices': staff_type_choices, 'error_message': error_message})
        except StaffType.DoesNotExist:
            # Create a new staff type
            staff_type = StaffType(name=name, description=description)
            staff_type.save()
            return redirect('staff_type_list')
    
    return render(request, 'root_template/create_staff_type.html', {'staff_type_choices': staff_type_choices})


def edit_staff_type_root(request, name):
    staff_type = StaffType.objects.get(name=name)
    if request.method == 'POST':
        staff_type.name = request.POST.get('name')
        staff_type. description = request.POST.get('description')
        staff_type.save()
        return redirect('staff_type_list')
    return render(request, 'root_template/edit_staff_type_root.html', {'staff_type': staff_type})


def delete_staff_type_root(request, name):
    staff_type = StaffType.objects.get(name=name)
    if request.method == 'POST':
        staff_type.delete()
        return redirect('staff_type_list')
    return render(request, 'root_template/delete_staff_type_root.html', {'staff_type': staff_type})


def suspend_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        # Handle the POST request to confirm the suspension
        company.is_suspended = True
        company.save()
        # Optionally, you can add a success message
        messages.success(
            request, f'Company "{company.name}" has been suspended.')
        # Redirect to the company list or any other appropriate page
        return redirect('company_list')

    # Render the confirmation page for suspending the company
    return render(request, 'root_template/suspend_company_confirm.html', {'company': company})


@login_required
def assign_staff_type(request, company_id):
    company = get_object_or_404(Company, company_id=company_id)
    error_message = ''  # Initialize error_message to an empty string

    if request.method == "POST":
        staff_type_names = request.POST.getlist('staff_type_name')

        # Clear previous assignments for the company
        company.staff_types.clear()

        # Update assignment status for the selected staff types
        for staff_type_name in staff_type_names:
            try:
                staff_type = StaffType.objects.get(name=staff_type_name)
                company.staff_types.add(staff_type)
                messages.success(request, f'Staff type "{staff_type_name}" assigned successfully!')
            except StaffType.DoesNotExist:
                error_message = f'Staff type "{staff_type_name}" not found'

        return redirect('assigned_staff_types_list')

    staff_type_choices = StaffType.STAFF_TYPE_CHOICES
    staff_types = StaffType.objects.all()

    # Get the staff types already assigned to the company
    assigned_staff_types = company.staff_types.values_list('name', flat=True)

    return render(
        request,
        'root_template/assign_staff_type.html',
        {
            'company': company,
            'staff_types': staff_types,
            'error_message': error_message,
            'staff_type_choices': staff_type_choices,
            'assigned_staff_types': assigned_staff_types,
        }
    )

def assigned_staff_types_list(request):
    companies = Company.objects.all()

    return render(request, 'root_template/assigned_staff_types_list.html', {
        'companies': companies,
    })


@login_required
def assigned_staff_type_edit(request, company_id):
    company = get_object_or_404(Company, company_id=company_id)

    if request.method == "POST":
        staff_user_id = request.POST.get('staff_user_id')
        staff_type_name = request.POST.get('staff_type_name')

        try:
            staff_user = CustomUser.objects.get(id=staff_user_id, company=company, user_type=2)
            staff_type = StaffType.objects.get(name=staff_type_name)
            staff_user.staff_type = staff_type
            staff_user.save()

            messages.success(request, 'Staff type updated successfully!')
            return redirect('assigned_staff_types_list')

        except CustomUser.DoesNotExist:
            messages.error(request, 'Staff user not found')
        except StaffType.DoesNotExist:
            messages.error(request, 'Staff type not found')

    staff_types = StaffType.objects.all()
    staff_users = company.custom_users.filter(user_type=2)

    return render(request, 'root_template/assigned_staff_type_edit.html', {'company': company, 'staff_types': staff_types, 'staff_users': staff_users})



@login_required
def dashboard(request):
    # Get user-specific data (assuming you have a CustomUser model)
    user = request.user
    booked_tickets = Booking.objects.filter(user=user, is_booked=True)
    
    # Get general data for the dashboard
    total_bookings = Booking.objects.count()
    total_coaches = Coach.objects.count()
    total_routes = Route.objects.count()
    total_companies = Company.objects.count()
    total_staffs = Staffs.objects.count()
    total_customers = Customers.objects.count()
    total_bus=Bus.objects.count()
    total_ticket_sales = Booking.objects.filter(is_paid=True).count()

    upcoming_journeys = JourneyDateHistory.objects.filter(
        journey_date__gte=date.today(), upcoming_schedule=True
    )

    context = {
        'user': user,
        'booked_tickets': booked_tickets,
        'total_bookings': total_bookings,
        'total_coaches': total_coaches,
        'total_routes': total_routes,
        'total_companies': total_companies,
        'total_staffs': total_staffs,
        'total_customers': total_customers,
        'total_ticket_sales': total_ticket_sales,
        'upcoming_journeys': upcoming_journeys,
        'total_bus': total_bus
    }

    return render(request, 'root_template/home_content.html', context)