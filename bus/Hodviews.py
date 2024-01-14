from .models import Counter, BusStop, Route
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
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
from .decorators import user_type_required
from accounts.models import FinancialTransaction,Bank
from django.contrib.contenttypes.models import ContentType



from django.db import transaction

def set_language(request, language_code):
    if language_code in [lang[0] for lang in settings.LANGUAGES]:
        request.session[translation.LANGUAGE_SESSION_KEY] = language_code
        translation.activate(language_code)
    return redirect(request.META.get('HTTP_REFERER'))


@user_type_required(user_types=[1, 2]) 
def create_user(request):
    company_user = request.user
    company = company_user.company
    company = Company.objects.get(id=company.id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
        nid_number = request.POST.get('nid_number')
        city_name = request.POST.get('city_name')
        zip_code = request.POST.get('zip_code')
        nid_image = request.FILES.get('nid_image')
        address = request.POST.get('address')
      

        names = full_name.split()
        first_name = names[0] if names else ''
        last_name = ' '.join(names[1:]) if names else ''

        try:
            user = CustomUser.objects.create_user(
                username='None',
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                profile_picture=profile_picture,
                nid_number=nid_number,
                city_name=city_name,
                zip_code=zip_code,
                nid_image=nid_image,
                address=address,
                user_type=2,
                company=company
            )
            user.set_password(password)
            user.save()

            # No need to fetch the staff_type if you're not using it here
            Staffs.objects.create(
                admin=user,
                company=company,
                # staff_type=staff_type,  # Remove this line
                address=address
            )

            # Ensure user_type has a valid value, default to 1 if None
            

            # user_group_name = CustomUser.USER_TYPE_CHOICES[user_type - 1][1] + 's'
            # user_group, created = Group.objects.get_or_create(
            #     name=user_group_name)
            # user.groups.add(user_group)

            messages.success(
                request, f'User "{user.username}" created successfully.')
            # Redirect to user list page after successful creation
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')

    return render(request, 'hod_template/user_list.html')

@user_type_required(user_types=[1, 2]) 
def assign_permissions(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    staff_types = StaffType.objects.all()
    custom_permissions = Permission.objects.filter(content_type__app_label='inventory')
    permission_bus = Permission.objects.filter(content_type__app_label='bus')
    permission_model_list = []
    bus_permissions = ['bus', 'seat']
    route_permissions = ['district', 'division','thana', 'union', 'upazila']
    coach_permissions = ['boardingpoint', 'coach', 'journeydatehistory']
    counter_permissions = ['counter', 'busstop']
    booking_permissions = ['booking', 'ticketbooking', 'cancelticket']
    payment_permissions = ['payment', 'paymentmethod', 'refund']
    user_permissions = ['users', 'customuser', 'rootuser', 'staffs', 'stafftype', 'profile']
    for permission in permission_bus:
        # print the app name of the permission
        # print('permission: ', permission.content_type.model)
        permission_model = permission.content_type.model
        if permission_model not in permission_model_list:
            permission_model_list.append(permission_model)
    for permission_model_name in permission_model_list:
        # if there is a string `route` in the model name (permission_model_name)
        if 'route' in permission_model_name or permission_model_name in route_permissions:
            # print('route words: ', permission_model_name)
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Route')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            route_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', route_perms)
            custom_permisssion.permissions.add(*route_perms)
            custom_permisssion.save()
        # create bus permissions
        elif permission_model_name in bus_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Bus')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            bus_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', bus_perms)
            custom_permisssion.permissions.add(*bus_perms)
            custom_permisssion.save()
        # create coach permissions
        elif permission_model_name in coach_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Coach')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            coach_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', coach_perms)
            custom_permisssion.permissions.add(*coach_perms)
            custom_permisssion.save()
        # counter coach permissions
        elif permission_model_name in counter_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Counter')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            counter_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', counter_perms)
            custom_permisssion.permissions.add(*counter_perms)
            custom_permisssion.save()
        # booking coach permissions
        elif permission_model_name in booking_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Booking')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            booking_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', booking_perms)
            custom_permisssion.permissions.add(*booking_perms)
            custom_permisssion.save()
        # payment coach permissions
        elif permission_model_name in payment_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Payment')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            payment_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', payment_perms)
            custom_permisssion.permissions.add(*payment_perms)
            custom_permisssion.save()
        # user coach permissions
        elif permission_model_name in user_permissions:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Users')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            user_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', user_perms)
            custom_permisssion.permissions.add(*user_perms)
            custom_permisssion.save()
        else:
            permission_category, created_at = PermissionCategory.objects.get_or_create(name='Miscelleneous')
            custom_permisssion, created_at = CustomPermission.objects.get_or_create(category=permission_category)
            miscelleneous_perms = Permission.objects.filter(content_type__model=permission_model_name)
            # print('route_permissions: ', user_perms)
            custom_permisssion.permissions.add(*miscelleneous_perms)
            custom_permisssion.save()
            # for route_perm in route_perms:
            #     # print(f"{permission} permission: {route_perm.id}")
            #     print('route_perm after: ', route_perm.id)
            #     # custom_permisssion.permissions.add(route_perm)
    print('permission_model_list: ', permission_model_list)
    if request.method == 'POST':
        selected_permissions = request.POST.getlist('selected_permissions')
        department_permissions_list = request.POST.getlist('department_permissions')
        department_permissions = [item.lower() for item in department_permissions_list]
        print('selected_permissions: ', selected_permissions)
        print('department_permissions: ', department_permissions)
        try:
            user.user_permissions.clear()  # Clear existing permissions
            for permission_id in selected_permissions:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)
            messages.success(
                request, f'Permissions assigned to user "{user.username}" successfully.')
            try:
                # staff_department_permissions = []
                if department_permissions_list:
                    for department_name in department_permissions_list:
                        staff_types = StaffType.objects.get(name=department_name)
                        user.staff_type = staff_types
                        user.save()
                for department_permission in department_permissions:
                    inventory_permissions = Permission.objects.filter(content_type__app_label=department_permission)
                    for inventory_permission in inventory_permissions:
                        print('permission id: ', inventory_permission.id)
                        department_permission_id = inventory_permission.id
                        department_perms = Permission.objects.get(id=department_permission_id)
                        user.user_permissions.add(department_perms)
                # for staff_department_permission in staff_department_permissions:
                #     print('staff_department_permission: ', staff_department_permission)00
                # for inventory_permission in inventory_permissions:
                #     print('permission id: ', inventory_permission.id)
            except Exception as e:
                messages.error(request, f'Error assigning permissions: {e}')
        except Exception as e:
            messages.error(request, f'Error assigning permissions: {e}')
        # Redirect to user list page after assigning permissions
        return redirect('user_list')
    permission_categories = PermissionCategory.objects.all()
    permissions_by_category = {}
    for category in permission_categories:
        permissions = Permission.objects.filter(
            custompermission__category=category)
        permissions_by_category[category] = permissions
    context = {
        'user': user,
        'permission_categories': permission_categories,
        'permissions_by_category': permissions_by_category,
        'staff_types': staff_types
    }
    return render(request, 'hod_template/assign_permissions.html', context)

@user_type_required(user_types=[1, 2]) 
def user_list(request):
    # Get the currently logged-in user
    current_user = get_user(request)

    # Filter users by user type 1 and 2 (exclude user type 0 and 3) and exclude the current user
    users = CustomUser.objects.filter(Q(user_type=1) | Q(user_type=2)).exclude(id=current_user.id)
    
    return render(request, 'hod_template/manage_user.html', {'users': users})

@user_type_required(user_types=[1, 2]) 
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        # Process the form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_picture = request.FILES.get('profile_picture')
        nid_number = request.POST.get('nid_number')
        city_name = request.POST.get('city_name')
        zip_code = request.POST.get('zip_code')
        nid_image = request.FILES.get('nid_image')
        address = request.POST.get('address')
        user_type = int(request.POST.get('user_type'))
        selected_permissions_codenames = request.POST.get(
            'selected_permissions_input').split(',')
        selected_permissions = Permission.objects.filter(
            codename__in=selected_permissions_codenames)

        # Update user data
        user.username = username
        user.email = email
        user.phone_number = phone_number
        user.user_type = user_type
        user.nid_number = nid_number
        user.city_name = city_name
        user.zip_code = zip_code
        user.address = address

        if profile_picture:
            user.profile_picture = profile_picture

        if nid_image:
            user.nid_image = nid_image

        user.save()

        # Update user's permissions
        user.user_permissions.set(selected_permissions)

        messages.success(
            request, f'User "{user.username}" updated successfully.')
        return redirect('user_detail', user_id=user.id)

    # Get user's selected permissions
    selected_permissions = user.user_permissions.all()

    # Get all available permissions
    all_permissions = Permission.objects.all()

    # Get unselected permissions by excluding selected ones
    unselected_permissions = all_permissions.exclude(
        id__in=selected_permissions)

    return render(request, 'hod_template/update_user.html', {
        'user': user,
        'selected_permissions': selected_permissions,
        'unselected_permissions': unselected_permissions,
    })

@user_type_required(user_types=[1, 2]) 
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'user not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@user_type_required(user_types=[1, 2]) 
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_permissions = user.user_permissions.all()  # Retrieve user's permissions
    return render(request, 'hod_template/user_detail.html', {'user': user, 'user_permissions': user_permissions})

@user_type_required(user_types=[1, 2]) 
def admin_profile(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})

@user_type_required(user_types=[1, 2]) 
def admin_profile_save(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                customuser.profile_picture = profile_picture

            # Handle password change
            if password:
                customuser.set_password(password)

            customuser.save()
            messages.success(request, "Successfully Updated Profile")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")

    return redirect("admin_profile")

@user_type_required(user_types=[1, 2]) 
def get_customer_data(request):
    user = request.user
    start_date = datetime.today() - timedelta(days=30)  # 30 days ago
    end_date = datetime.today()
    daily_customer_counts = []

    if user.user_type == 1:
        current_date = start_date
        while current_date <= end_date:
            daily_count = Customers.objects.filter(
                created_at__date=current_date.date()).count()
            daily_customer_counts.append(daily_count)
            current_date += timedelta(days=1)
    elif user.user_type == 2:
        # Get the associated Staffs instance
        staff_instance = Staffs.objects.get(admin=user)

        # Get the Coach objects associated with the staff's admin user
        coach_objects = Coach.objects.filter(
            staffs__admin=staff_instance.admin)
        coach_ids = coach_objects.values_list('id', flat=True)

        current_date = start_date
        while current_date <= end_date:
            daily_count = Booking.objects.filter(
                coach_id__in=coach_ids,
                journey_date__journey_date=current_date.date()
            ).values('customer').distinct().count()
            daily_customer_counts.append(daily_count)
            current_date += timedelta(days=1)

    data = {
        "daily_customer_counts": daily_customer_counts
    }

    return JsonResponse(data)

@user_type_required(user_types=[1, 2]) 
def route_booking_count_graph(request):
    user = request.user
    if user.user_type == 1:
        routes = Route.objects.annotate(booking_count=Count('parts__booking'))

        route_data = [
            {'route_name': route.__str__(), 'booking_count': route.booking_count}
            for route in routes
        ]
    else:
        route_data = [
            {'route_name': route.__str__(), 'booking_count': None}
            for route in Route.objects.all()
        ]

    return JsonResponse({'route_data': route_data})

@user_type_required(user_types=[1, 2]) 
@login_required
def admin_home(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if user.user_type not in [1, 2]:
        return redirect('index')
    current_year = date.today().year
    current_month = date.today().month
    customer_count = Customers.objects.filter(company=company).count()
    staff_count = Staffs.objects.filter(company=company).count()
    bus_count = Bus.objects.filter(company=company).count()
    user_count = CustomUser.objects.filter(company=company).count()
    current_year_sales = Booking.objects.filter(
        journey_date__journey_date__year=current_year, company=company)
    current_year_sales_price = current_year_sales.aggregate(
        total=Sum('price')).get('total', 0)
    current_month_sales = Booking.objects.filter(
        journey_date__journey_date__year=current_year, journey_date__journey_date__month=current_month, company=company)
    current_month_sales_price = current_month_sales.aggregate(
        total=Sum('price')).get('total', 0)
    last_month_sales = Booking.objects.filter(
        journey_date__journey_date__year=current_year, journey_date__journey_date__month=current_month-1, company=company)
    last_month_sales_price = last_month_sales.aggregate(
        total=Sum('price')).get('total', 0)
    if user.user_type == 2:
        staff_ticket_booking = Booking.objects.filter(user=user, company=company)
        customer_count = staff_ticket_booking.count()
        total_price = staff_ticket_booking.aggregate(
            total=Sum('price')).get('total', 0)
        print('staff_ticket_sales: ', total_price)
        print('user type: ', user.user_type)
        print('staff_ticket_booking_count: ', customer_count)
    else:
        total_price = Booking.objects.aggregate(
            total=Sum('price')).get('total', 0)
    # ticket sales by individual staff
    staff_data = []
    print('total price: ', total_price)
    # Assuming user_type 2 corresponds to staff
    # staff_members = CustomUser.objects.filter(user_type=2)
    # for staff in staff_members:
    #     total_bookings = Booking.objects.filter(user=staff).count()
    #     staff_data.append({
    #         'name': staff.username,
    #         'total_bookings': total_bookings
    #     })
    try:
        counter_instance = Counter.objects.get(manager=user)
        credit_balance = counter_instance.credit_balance
    except Counter.DoesNotExist:
        credit_balance = None 
    return render(request, "hod_template/home_content.html", {
        "customer_count": customer_count,
        "staff_count": staff_count,
        "bus_count": bus_count,
        "user_count": user_count,
        "total_price": total_price,
        "current_year_sales_price": current_year_sales_price,
        "credit_balance": credit_balance,
        # 'staff_ticket_booking_count': staff_ticket_booking_count
        # 'staff_ticket_sales': staff_ticket_sales
    })
@user_type_required(user_types=[1, 2]) 
@login_required
def admin_home_data(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    month_list = []
    current_year_monthly_price = []
    last_year_monthly_price = []
    current_year = date.today().year
    current_month = date.today().month
    sales_record_dict = {}
    sales_record_dict[current_year] = {}
    sales_record_dict[current_year - 1] = {}
    all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                  'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in range(1, 13):
        booking_current_year_per_month = Booking.objects.filter(
            journey_date__journey_date__year=current_year, journey_date__journey_date__month=month, company=company)
        booking_last_year_per_month = Booking.objects.filter(
            journey_date__journey_date__year=current_year - 1, journey_date__journey_date__month=month, company=company)
        current_year_sales_price = booking_current_year_per_month.aggregate(
            total=Sum('price')).get('total', 0)
        last_year_sales_price = booking_last_year_per_month.aggregate(
            total=Sum('price')).get('total', 0)
        sales_month = all_months[month - 1]
        current_year_monthly_price.append(current_year_sales_price)
        last_year_monthly_price.append(last_year_sales_price)
        month_list.append(sales_month)
    sales_record_dict[current_year]['monthly_sales_price'] = current_year_monthly_price
    sales_record_dict[current_year]['month'] = month_list
    sales_record_dict[current_year -
                      1]['monthly_sales_price'] = last_year_monthly_price
    sales_record_dict[current_year - 1]['month'] = month_list
    # Count visitors
    ip_address = request.META.get('REMOTE_ADDR')
    # Process unauthenticated visitors
    if not request.user.is_authenticated:
        visitor = Visitor.objects.create(ip_address=ip_address, company=company)
        visitor.date_visited = datetime.now()
        visitor.save()
    # Process authenticated visitors
    else:
        user = request.user
        visitor = Visitor.objects.create(user=user)
        visitor.ip_address = ip_address
        visitor.date_visited = datetime.now()
        visitor.save()
    visitors_count = Visitor.objects.filter(company=company).count()
    data = {
        'booking_data': sales_record_dict,
        'current_year': current_year,
        'last_year': current_year - 1,
        'visitors_count': visitors_count
    }
    return JsonResponse(data)

@user_type_required(user_types=[1, 2]) 
def staff_booking_data(request):
    staff_data = []
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    # Assuming user_type 2 corresponds to staff
    staff_members = CustomUser.objects.filter(user_type=2, company=company)
    for staff in staff_members:
        total_bookings = Booking.objects.filter(user=staff, company=company).count()
        staff_data.append({
            'name': staff.username,
            'total_bookings': total_bookings
        })

    data = {
        'staff_data': staff_data
    }

    return JsonResponse(data)

@user_type_required(user_types=[1, 2]) 
def payment_method_booking_count(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    payment_method_data = []

    if user.user_type == 1:
        payment_methods = PaymentMethod.objects.filter(company=company)
        for method in payment_methods:
            count = Booking.objects.filter(
                payment_method=method, is_booked=True, company=company).count()
            payment_method_data.append({"method": method.name, "count": count})
    elif user.user_type == 2:
        try:
            staff_booked_coach_ids = Booking.objects.filter(
                user=user, is_booked=True, company=company
            ).values_list('coach_id', flat=True).distinct()

            payment_methods = PaymentMethod.objects.filter(
                booking__coach_id__in=staff_booked_coach_ids, company=company
            ).distinct()

            for method in payment_methods:
                count = Booking.objects.filter(
                    user=user, coach_id__in=staff_booked_coach_ids, payment_method=method, is_booked=True, company=company
                ).count()
                payment_method_data.append(
                    {"method": method.name, "count": count})
        except Booking.DoesNotExist:
            pass  # Handle the case where the user hasn't made any bookings

    response_data = {"payment_method_data": payment_method_data}
    return JsonResponse(response_data)

@user_type_required(user_types=[1, 2]) 
def booking_activity(request):
    period = request.GET.get('period')
    today = date.today()

    if period == 'today':
        clicks = Click.objects.filter(date__date=today)
    elif period == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        clicks = Click.objects.filter(date__date__range=[week_start, week_end])
    elif period == 'month':
        month_start = date(today.year, today.month, 1)
        month_end = date(today.year, today.month + 1, 1) - timedelta(days=1)
        clicks = Click.objects.filter(
            date__date__range=[month_start, month_end])
    else:
        
        clicks = Click.objects.filter(date__date=today)

    return render(request, 'hod_template/booking_activity.html', {'clicks': clicks})

@user_type_required(user_types=[1, 2]) 
def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

@user_type_required(user_types=[1, 2]) 
def add_staff_save(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        phone = request.POST.get("phone_number")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2,
                phone_number=phone,
                company=company
            )
            staff, created = Staffs.objects.get_or_create(admin=user)
            staff.address = address
            staff.save()

            if created:
                messages.success(request, "Successfully Added Staff")
            else:
                messages.success(request, "Staff added successfully")

            return HttpResponseRedirect(reverse("add_staff"))
        except IntegrityError:
            messages.error(
                request, "Username or email already exists. Please choose a different one.")
            return HttpResponseRedirect(reverse("add_staff"))
        except Exception as e:
            messages.error(request, f"Failed to Add Staff. Error: {str(e)}")
            return HttpResponseRedirect(reverse("add_staff"))

@user_type_required(user_types=[1, 2]) 
def add_district(request):
    if request.method == 'POST':
        name = request.POST['name']
        if District.objects.filter(name=name).exists():
            messages.error(request, 'District already exists')
        else:
            District.objects.create(name=name)
            messages.success(request, 'District added successfully')

    return render(request, 'hod_template/add_district.html')

@user_type_required(user_types=[1, 2]) 
def add_district_save(request):
    if request.method == 'POST':
        name = request.POST['name']
        if District.objects.filter(name=name).exists():
            messages.error(request, 'District already exists')
        else:
            District.objects.create(name=name)
            messages.success(request, 'District added successfully')
    return redirect('add_district')

@user_type_required(user_types=[1, 2]) 
def manage_staff(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    staffs = Staffs.objects.filter(company=company)
    return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})

@user_type_required(user_types=[1, 2]) 
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staffs, id=staff_id)

    if request.method == 'POST':
        # Retrieve the updated data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')
        address = request.POST.get('address')

        # Validate the required fields
        if not first_name or not last_name or not email or not phone_number or not username or not address:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('edit_staff', staff_id=staff_id)

        # Update the staff member's information
        user = staff.admin
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        staff.phone_number = phone_number
        staff.address = address
        staff.save()

        messages.success(request, 'Staff information updated successfully!')
        return redirect('manage_staff')

    return render(request, 'hod_template/edit_staff_template.html', {'staff': staff, 'staff_id': staff_id})

@user_type_required(user_types=[1, 2]) 
def delete_staff(request, staff_id):
    # Use Staffs instead of staff
    staff = get_object_or_404(Staffs, id=staff_id)

    if request.method == 'POST':
        # Delete the staff object
        staff.delete()

        messages.success(request, 'Staff deleted successfully!')
        return redirect('manage_staff')

    return render(request, 'hod_template/delete_staff.html', {'staff': staff})


@csrf_exempt
def check_email_exist(request):
    user = request.user
 
   
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username, company=company).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_phone_number_exist(request):
    user = request.user

    
    phone_number = request.POST.get("phone_number")
    user_obj = CustomUser.objects.filter(phone_number=phone_number).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@user_type_required(user_types=[1, 2])
def add_counter(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    with open('bus/static/json/divisions.json', 'r', encoding='utf-8') as district_file:
        divisions_data = json.load(district_file)

    divisions_list = [{'division_id': division['id'], 'division_name': division['name']}
                      for division in divisions_data['divisions']]

    # Sort divisions by division names
    divisions = sorted(divisions_list, key=lambda x: x['division_name'])

    # Fetch the list of staff members
    staff_members = CustomUser.objects.filter(user_type=2)  # Get users with user_type 2

    context = {
        'divisions': divisions,
        'staff_members': staff_members
    }

    return render(request, "hod_template/add_counter.html", context)

@user_type_required(user_types=[1, 2])
def add_counter_save(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        data = json.loads(request.body)
        division_name = data['division_name']
        district_name = data['district_name']
        upazila_name = data['upazila_name']
        union_name = data['union_name']
        thana_name = data['thana']
        counter_name = data['name']

        address = data['address']
        phone_numbers = data['phone_numbers']
        manager_id = data['manager']  # Use 'manager' key to get the manager's ID

        # Fetch the selected manager user instance
        manager_user = CustomUser.objects.get(id=manager_id)

        response_data = {}

        if division_name == '' or district_name == '' or thana_name == '' or counter_name == '' or address == '' or phone_numbers == '':
            response_data['error'] = 'Please fill out all the fields'
            return JsonResponse(response_data, status=400)

        else:
            division, created_at = Division.objects.get_or_create(
                name=division_name)
            district, created_at = District.objects.get_or_create(
                name=district_name, division=division)
            upazila, created_at = Upazila.objects.get_or_create(
                name=upazila_name, division=division, district=district)
            union, created_at = Union.objects.get_or_create(
                name=union_name, division=division, district=district, upazila=upazila)
            thana, created_at = Thana.objects.get_or_create(
                name=thana_name, division=division, district=district)

            counter = Counter.objects.create(
                name=counter_name,
                manager=manager_user,  # Set the manager field as the user instance
                district=district,
                thana=thana,
                union=union,
                address=address,
                phone_numbers=phone_numbers,
                company=company
            )

            response_data['success'] = f"Counter created successfully with name: {counter_name}"

            return JsonResponse(response_data)

    messages.success(request, 'Counter added successfully!')
    return redirect('add_counter')


@user_type_required(user_types=[1, 2]) 
def districts(request):
    if request.method == 'GET' and 'division_id' in request.GET:
        division_id = request.GET['division_id']
        # print('division id: ', division_id)

        with open('bus/static/json/districts.json', 'r', encoding='utf-8') as district_file:
            districts_data = json.load(district_file)
        district_list = [{'district_id': district['id'], 'district_name': district['name']}
                         for district in districts_data['districts'] if district['division_id'] == division_id]

        # sort the  district by its name
        districts = sorted(district_list, key=lambda x: x['district_name'])
        first_district = districts[0]
        print('first_district: ', first_district['district_id'])
        # print('District Name: ', districts)

        context = {'districts': districts}
        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_type_required(user_types=[1, 2]) 
def thanas(request):
    if request.method == 'GET' and 'district_id' in request.GET:
        district_id = request.GET['district_id']
        print('district_id: ', district_id)

        with open('bus/static/json/thana.json', 'r', encoding='utf-8') as thana_file:
            thanas_data = json.load(thana_file)

        thana_list = []
        # upazila = {}

        for thana_data in thanas_data['thana']:
            if thana_data['district_id'] == district_id:
                upazila_dict = {
                    'thana_name': thana_data['thana']}
                thana_list.append(upazila_dict)

        # sort the thana by its names
        thana = sorted(thana_list, key=lambda x: x['thana_name'])
        print('thanas_data_list: ', thana)

        context = {'thana': thana}

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_type_required(user_types=[1, 2]) 


def manage_counters(request):
    user = request.user
    company = user.company

    counters = Counter.objects.filter(company=company)

    for counter in counters:
        transactions = FinancialTransaction.objects.filter(
            content_type=ContentType.objects.get_for_model(counter),
            object_id=counter.id  # Use the ID of the Counter, not manager username
        )
        print(f"Counter: {counter.name}, Manager: {counter.manager.username}")
        for transaction in transactions:
            print(f"Transaction: Amount={transaction.amount}")
        credit_balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        counter.credit_balance = credit_balance
        counter.save()

    context = {
        'counters': counters
    }
    return render(request, 'hod_template/manage_counters.html', context)

@user_type_required(user_types=[1, 2]) 
def counter_details(request, counter_id):
    counter = get_object_or_404(Counter, id=counter_id)

    context = {
        'counter': counter
    }
    return render(request, 'hod_template/counter_details.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_counter(request, counter_id):
    if request.method == 'POST':
        try:
            counter = Counter.objects.get(pk=counter_id)
            counter.delete()
            return JsonResponse({'success': True})
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'user not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@user_type_required(user_types=[1, 2]) 
def edit_counter(request, counter_id):
    counter = get_object_or_404(Counter, id=counter_id)
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        counter.name = request.POST['name']
        counter.manager = request.POST['manager']
        counter.district = request.POST['district']
        counter.thana = request.POST['thana']
        counter.address = request.POST['address']
        counter.phone_numbers = request.POST['phone_numbers']

        staff_id = request.POST.get('staff')
        if staff_id:
            staff = Staffs.objects.get(id=staff_id)
            counter.staff = staff
            counter.manager = staff.admin.username  # Assign the manager's username

        counter.save()
        return redirect('manage_counters')  # Redirect to the appropriate URL

    staff_members = Staffs.objects.filter(company=company)
    context = {
        'counter': counter,
        'staff_members': staff_members,
    }
    return render(request, 'hod_template/edit_counter.html', context)

@user_type_required(user_types=[1, 2]) 
def upazilas(request):
    if request.method == 'GET' and 'district_id' in request.GET:
        district_id = request.GET['district_id']
        print('district_id: ', district_id)

        with open('bus/static/json/bd-districts.json', 'r', encoding='utf-8') as district_file:
            district_data = json.load(district_file)

        with open('bus/static/json/upazilas.json', 'r', encoding='utf-8') as upazilas_file:
            upazilas_data = json.load(upazilas_file)

        upazilas = []
        # upazila = {}

        for upazila_data in upazilas_data['upazilas']:
            if upazila_data['district_id'] == district_id:
                upazila_dict = {
                    'upazila_id': upazila_data['id'], 'upazila_name': upazila_data['name']}
                upazilas.append(upazila_dict)
        print('upazila_data_list: ', upazilas)

        context = {'upazilas': upazilas}

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_type_required(user_types=[1, 2]) 
def unions(request):
    if request.method == 'GET' and 'upazila_id' in request.GET:
        upazila_id = request.GET['upazila_id']

        with open('bus/static/json/unions.json', 'r', encoding='utf-8') as unions_file:
            unions_data = json.load(unions_file)

        unions = [{'union_id': union['id'], 'union_name':union['name']}
                  for union in unions_data['unions'] if union['upazilla_id'] == upazila_id]
        context = {'unions': unions}

        return JsonResponse(context, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_type_required(user_types=[1, 2]) 
def add_faq_save(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    category_id = request.POST.get('category')
    category = Category.objects.get(id=category_id)

    question = request.POST.get('question')
    answer = request.POST.get('answer')
    faq = FAQ.objects.create(
        category=category,
        question=question,
        answer=answer,

    )
    messages.success(request, 'Add FAQ! successfully')
    return redirect('add_faq')

@user_type_required(user_types=[1, 2]) 
def add_category(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'POST':
        name = request.POST['name']
        if Category.objects.filter(name=name, company=company).exists():
            messages.error(request, 'District already exists')
            return redirect('add_category')
        else:
            Category.objects.create(name=name, company=company)
            messages.success(request, 'Category added successfully')
            return redirect('add_category')
    return render(request, 'hod_template/add_category.html')

@user_type_required(user_types=[1, 2]) 
def add_category_save(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'POST':
        name = request.POST['name']
        if Category.objects.filter(name=name, company=company).exists():
            messages.error(request, 'Category already exists')
        else:
            Category.objects.create(name=name, company=company)
            messages.success(request, 'Category added successfully')
    return redirect('add_category')

@user_type_required(user_types=[1, 2]) 
def add_faq(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    category = Category.objects.filter(company=company)
    return render(request, "hod_template/add_faq.html", {'category': category})

@user_type_required(user_types=[1, 2]) 
def edit_faq(request, faq_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    faq = get_object_or_404(FAQ, pk=faq_id)
    categories = Category.objects.filter(company=company)
    if request.method == 'POST':
        category_id = request.POST.get('category')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        category = get_object_or_404(Category, pk=category_id)
        faq.category = category
        faq.question = question
        faq.answer = answer
        faq.save()
        return redirect('faq_list')
    context = {
        'faq': faq,
        'categories': categories
    }
    return render(request, 'hod_template/edit_faq.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, pk=faq_id)
    if request.method == 'POST':
        faq.delete()
        return redirect('faq_list')
    context = {
        'faq': faq
    }
    return render(request, 'hod_template/delete_faq.html', context)

@user_type_required(user_types=[1, 2]) 
def faq_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    faqs = FAQ.objects.filter(company=company)
    context = {
        'faqs': faqs
    }
    return render(request, 'hod_template/faq_list.html', context)

# @user_type_required(user_types=[1, 2]) 
def get_default_cancellation_policy(company):
    try:
        coach = Coach.objects.filter(company=company).first()
        if coach is not None:
            return coach.cancellation_policy
        else:
            return 'We Provide You All TLD Domain Services In Low Cost. Just you can make an order using our online billing, we will activate your domain within a few minutes.'
    except Coach.DoesNotExist:
        return 'We Provide You All TLD Domain Services In Low Cost. Just you can make an order using our online billing, we will activate your domain within a few minutes.'

@login_required
@user_type_required(user_types=[1, 2])
def add_coach(request):
    if request.user.is_authenticated:
        user = request.user
        company = user.company
        company = Company.objects.get(id=company.id)
        # Fetch available buses and routes for rendering in the form
        buses = Bus.objects.filter(company=company)
        routes = Route.objects.filter(company=company)
        facilities = Facility.objects.filter(company=company)
        default_cancellation_policy = get_default_cancellation_policy(company)
        return render(request, 'hod_template/add_coach.html', {'buses': buses, 'routes': routes, 'facilities': facilities, 'default_cancellation_policy': default_cancellation_policy})

@user_type_required(user_types=[1, 2]) 
def get_coach_route_price(request):
    if request.method == 'GET' and 'route_id' in request.GET:
        route_id = request.GET['route_id']
        route = Route.objects.get(id=route_id)
        route_points = route.split_into_parts
        possible_routes = []

        for i in range(len(route_points)):
            for j in range(i + 1, len(route_points)):
                single_route = {
                    'start_point': route_points[i].name,
                    'end_point': route_points[j].name
                }
                possible_routes.append(single_route)

        print('possible_routes: ', possible_routes)
        print('route_id: ', route_id)
        print('route: ', route)
    return JsonResponse(possible_routes, safe=False)

@user_type_required(user_types=[1, 2]) 
def coach_save(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'POST':
        data = json.loads(request.body)
        coach_name = data['coachmodelname']
        coach_number = data['coachnumber']
        coach_type = data['coachtype']
        arrival_time = data['arrivaltime']
        cancellation_policy = data['cancellation_policy']
        facilities_list = data['facilities']
        boarding_points_list = data['boarding_points']
        bus_id = data['bus_id']
        route_id = data['route_ids']
        route_part_data = data['route_part_data']

        response_data = {}

        if route_id:
            bus = Bus.objects.get(id=bus_id)
            try:
                route = Route.objects.get(id=route_id)
            except:
                response_data = {'error': 'Route does not exist'}

            route_points = route.split_into_parts
            possible_routes = []

            for i in range(len(route_points)):
                for j in range(i + 1, len(route_points)):
                    single_route = {
                        'start_point': route_points[i].name,
                        'end_point': route_points[j].name
                    }
                    possible_routes.append(single_route)
            print('possible_routes: ', possible_routes)

            # for route_data in route_part_data:
            #     for possible_route in possible_routes:
            #         if route_data['start_point'] == possible_route['start_point'] and route_data['end_point'] == possible_route['end_point']:
            #             print('True')

            # matches if the route parts from the fromt end matches with the route parts in the backend
            route_data_set = {(route['start_point'], route['end_point'])
                              for route in route_part_data}
            print('route_data_set: ', route_data_set)
            possible_routes_set = {
                (route['start_point'], route['end_point']) for route in possible_routes}

            if coach_name and coach_number and coach_type and arrival_time and cancellation_policy and facilities_list and boarding_points_list:
                facilities = [Facility.objects.get(
                    id=facility) for facility in facilities_list]
                boarding_points = [BoardingPoint.objects.get(
                    id=boarding_point) for boarding_point in boarding_points_list]
                print('facilities: ', facilities)
                print('boarding_points: ', boarding_points)
                coaches = Coach.objects.filter(company=company)
                coach_number_list = [str(each_coach.coachnumber)
                                     for each_coach in coaches]

                if str(coach_number) in coach_number_list:
                    response_data = {
                        'error': f"Coach number: {coach_number} already exists"}
                    return JsonResponse(response_data)

                else:
                    coach = Coach.objects.create(
                        bus=bus,
                        coachnumber=coach_number,
                        coachtype=coach_type,
                        coachmodelname=coach_name,
                        arrivaltime=arrival_time,
                        cancellation_policy=cancellation_policy,
                        company=company
                    )

                    coach.save()
                    coach.routes.add(route)
                    coach.facilities.set(facilities)
                    coach.boarding_points.set(boarding_points)

                if route_data_set == possible_routes_set:
                    for route_data in route_part_data:
                        route_part_start_point = route_data['start_point']
                        route_part_end_point = route_data['end_point']
                        price = route_data['price']

                        bus_stop_start_point = BusStop.objects.filter(
                            name__name=route_part_start_point, company=company).first()
                        bus_stop_end_point = BusStop.objects.filter(
                            name__name=route_part_end_point, company=company).first()

                        if not price:
                            continue

                        if bus_stop_start_point and bus_stop_end_point and price:
                            route_part = RoutePart.objects.create(
                                route=route,
                                start_point=bus_stop_start_point,
                                end_point=bus_stop_end_point,
                                price=price,
                                coach=coach,
                                company=company
                            )

                            route_part.save()

                        else:
                            response_data = {'error': 'Route Id not found'}
                            return JsonResponse(response_data)

                else:
                    response_data = {'error': 'Route Part data does not exist'}
                    return JsonResponse(response_data)

            else:
                response_data = {'error': 'Please fill out all the details'}
                return JsonResponse(response_data)

        else:
            response_data = {'error': 'Route Id not found'}
            return JsonResponse(response_data)

        print('coach_name: ', coach_name)
        print('data: ', data)

        response_data = {
            'success': f"Coach Name: {coach.coachmodelname} and Coach number: {coach.coachnumber} saved successfully"}

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
    # If the request method is not POST, render the form
    # buses = Bus.objects.all()
    # routes = Route.objects.all()
    # facilities = Facility.objects.all()
    # default_cancellation_policy = get_default_cancellation_policy()
    # return render(request, 'hod_template/add_coach.html', {'buses': buses, 'routes': routes, 'facilities': facilities, 'default_cancellation_policy': default_cancellation_policy})

@login_required
# @user_type_required(user_types=[1, 2])
def busregi(request):
    if request.method == 'POST':
        form = BusRegistrationForm(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            seat_type_1 = form.cleaned_data.get('seat_type_1')
            seat_type_2 = form.cleaned_data.get('seat_type_2')
            seat_type_3 = form.cleaned_data.get('seat_type_3')
            number_or_column = form.cleaned_data.get('number_or_column')
            bus_number = form.cleaned_data.get('bus_number')
            extra_seat = form.cleaned_data.get('extra_seat')

            if request.user.is_authenticated:
                user = request.user
                print('user: ', user)
                company = user.company
                print('company: ', company)
                company = Company.objects.get(id=company.id)

                get_bus = Bus.objects.filter(bus_number=bus_number, company=company)

            if not get_bus:
                if seat_type_1 == number_or_column:
                    seat_type_2 = ''
                    seat_type_3 = ''
                elif seat_type_2 == number_or_column:
                    seat_type_1 = ''
                    seat_type_3 = ''
                elif seat_type_3 == number_or_column:
                    seat_type_1 = ''
                    seat_type_2 = ''
                if seat_type_1 and seat_type_2 and seat_type_3 and number_or_column:
                    if int(seat_type_1) + int(seat_type_2) + int(seat_type_3) != int(number_or_column):
                        form.add_error(
                            None, "The sum of seat type 1, seat type 2, and seat type 3 must be equal to Number Of Column.")
                        return render(request, 'hod_template/busregi.html', {'form': form})
                bus.seat_type_1 = seat_type_1
                bus.seat_type_2 = seat_type_2
                bus.seat_type_3 = seat_type_3
                # Check if the user is authenticated and update user-related fields

                bus.user = user
                bus.company = company
                bus.extra_seat = extra_seat
                bus.save()
                seat_types = []
                total_rows = int(number_or_column) // 4
                seat_type_1_count = 0
                if seat_type_1:
                    seat_type_1_count = int(seat_type_1)
                    seat_types.append({
                        'type': '1:1',
                        'seats': generate_seats('1:1', seat_type_1_count, 4),
                        'rows': generate_rows(seat_type_1_count),
                        'total_seats': seat_type_1_count * 4,
                    })
                seat_type_2_count = 0
                if seat_type_2:
                    seat_type_2_count = int(seat_type_2)
                    seat_types.append({
                        'type': '1:2',
                        'seats': generate_seats('1:2', seat_type_2_count, 4),
                        'rows': generate_rows(seat_type_2_count),
                        'total_seats': seat_type_2_count * 4,
                    })
                seat_type_3_count = 0
                if seat_type_3:
                    seat_type_3_count = int(seat_type_3)
                    seat_types.append({
                        'type': '2:2',
                        'seats': generate_seats('2:2', seat_type_3_count, 4),
                        'rows': generate_rows(seat_type_3_count),
                        'total_seats': seat_type_3_count * 4,
                    })
                mixed_seats = generate_seats(
                    'mixed', total_rows - seat_type_1_count - seat_type_2_count - seat_type_3_count, 4)
                seat_types.append({
                    'type': 'mixed',
                    'seats': mixed_seats,
                    'rows': generate_rows(total_rows - seat_type_1_count - seat_type_2_count - seat_type_3_count),
                    'total_seats': (total_rows - seat_type_1_count - seat_type_2_count - seat_type_3_count) * 4,
                })
                context = {
                    'form': form,
                    'success_message': 'Bus saved successfully.',
                    'seat_types': seat_types,
                    'total_rows': total_rows,
                }
                return render(request, 'hod_template/busregi.html', context)
            
            else:
                context = {
                    'form': form,
                    'success_message': 'Bus with same number already exists'
                }
                return render(request, 'hod_template/busregi.html', context)
    else:
        form = BusRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'hod_template/busregi.html', context)





# @user_type_required(user_types=[1, 2]) 
def generate_rows(quantity):
    rows = []
    for i in range(int(quantity)):
        rows.append(chr(65 + (i % 10)))
    return rows

# @user_type_required(user_types=[1, 2])
def generate_seats(seat_type, quantity, columns):
    seats = []
    if seat_type == '1:1':
        seat_number = 1
        for _ in range(int(quantity)):
            row = []
            for _ in range(columns):
                row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                seat_number += 2
            seats.append(row)
    elif seat_type == '1:2':
        seat_number = 1
        for _ in range(int(quantity)):
            row = []
            for i in range(columns):
                if i % 3 == 0:
                    row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                    seat_number += 1
                elif i % 3 == 1:
                    row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                    seat_number += 2
                else:
                    row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                    seat_number += 2
            seats.append(row)
    elif seat_type == '2:2':
        seat_number = 1
        for _ in range(int(quantity)):
            row = []
            for i in range(columns):
                if i % 3 == 0 or i % 3 == 1:
                    row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                    seat_number += 1
                else:
                    row.append('{}{}'.format(chr(65 + (_ % 10)), seat_number))
                    seat_number += 1
            seats.append(row)
    else:
        for _ in range(int(quantity)):
            seats.append(['None Seats'] * columns)
    return seats

# @user_type_required(user_types=[1, 2]) 
def generate_mixed_seats(bus, quantity, columns):
    seats = []
    seat_number = 1
    for _ in range(int(quantity)):
        row = []
        for i in range(columns):
            seat_type = i % 3
            seat = Seat(bus=bus, row_number=chr(65 + (_ % 10)),
                        seat_number=str(seat_number))
            if seat_type == 0:
                seat.seat_type = 'seat_type_1'
            elif seat_type == 1:
                seat.seat_type = 'seat_type_2'
            else:
                seat.seat_type = 'seat_type_3'
            row.append(seat)
            seat_number += 1
        seats.append(row)
    bus.total_seats = seat_number - 1
    bus.save()
    re
    
def bus_list(request):
    # Query all buses from the database
    buses = Bus.objects.all()


    context = {'buses': buses}
    

    return render(request, 'hod_template/buslist.html', context)



def delete_bus(request, bus_id):
    if request.method == 'POST':
        try:
            brand = Bus.objects.get(pk=bus_id)
            brand.delete()
            return JsonResponse({'success': True})
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Bus not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def view_bus(request, bus_id):
    # Retrieve the bus object or return a 404 error if it doesn't exist
    bus = get_object_or_404(Bus, id=bus_id)

    # Prepare the data to be serialized into JSON
    bus_data = {
        'bus_number': bus.bus_number,
        'bus_type': bus.get_bus_type_display(),
        'number_or_column': bus.number_or_column,
        'seat_type_1': bus.seat_type_1,
        'seat_type_2': bus.seat_type_2,
        'seat_type_3': bus.seat_type_3,
        'extra_seat': bus.get_extra_seat_display(),
        'total_seats': bus.total_seats,
        'class_type': bus.get_class_type_display(),
        # Add other fields as needed
    }

    # Return the data as JSON response
    return JsonResponse(bus_data)



@user_type_required(user_types=[1, 2]) 
def booking_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    today = date.today()
    # Get the next 5 days including today
    next_five_days = [today + timedelta(days=i) for i in range(6)]
    # Retrieve coaches that have journeys scheduled for today and the next 5 days
    coaches_for_next_six_days = Coach.objects.filter(
        journey_dates__journey_date__in=next_five_days
    ).distinct()
    # Annotate the coaches with the count of booked seats for the upcoming journey dates
    coaches_for_next_six_days = coaches_for_next_six_days.annotate(
        num_booked_seats=Sum(
            Case(
                When(booking__journey_date__journey_date__in=next_five_days,
                     booking__is_booked=True, company=company, then=1),
                default=Value(0),
                output_field=IntegerField()
            )
        )
    ).order_by('-num_booked_seats')  # Use negative value to sort in ascending order
    coach_details_list = []
    for coach in coaches_for_next_six_days:
        journey_date_obj = coach.journey_dates.filter(
            journey_date=today).first()  # Filter to include only coaches with a journey today
        if journey_date_obj:
            total_seats, remaining_seats = Booking.get_booked_seats(
                journey_date=journey_date_obj, coach=coach, company=company)
            booked_seats = total_seats - remaining_seats
            occupancy = (booked_seats / total_seats) * 100
            seat_occupancy = "{:.1f}".format(occupancy)
            upcoming_schedule = journey_date_obj.journey_date >= today
            # Fetch route parts for the coach
            route_parts = RoutePart.objects.filter(coach=coach)
            journey_date_details = {
                'coach': coach,
                'journey_date': journey_date_obj.journey_date,
                'total_seats': total_seats,
                'booked_seats': booked_seats,
                'remaining_seats': remaining_seats,
                'seat_occupancy': seat_occupancy,
                'upcoming_schedule': upcoming_schedule,
                'route_parts': route_parts  # Include route parts in the dictionary
            }
            coach_details_list.append(journey_date_details)
    # Sort the coach_details_list based on the remaining seats in descending order
    coach_details_list.sort(key=lambda x: x['booked_seats'], reverse=False)
    context = {
        'coach_details_list': coach_details_list,
        'next_five_days': next_five_days
    }
    return render(request, 'hod_template/booking_list.html', context)

@user_type_required(user_types=[1, 2]) 
def coach_details_by_date(request, journey_date_str):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    # Convert the journey_date_str from a string to a date object
    journey_date = date.fromisoformat(journey_date_str)
    # Retrieve coaches that have journeys scheduled for the given date
    coaches_for_date = Coach.objects.filter(
        journey_dates__journey_date=journey_date, company=company).distinct()
    coach_details_list = []
    for coach in coaches_for_date:
        # Find the JourneyDateHistory object for the given journey_date and coach
        journey_date_obj = coach.journey_dates.filter(
            journey_date=journey_date, company=company).first()
        if journey_date_obj:
            total_seats, remaining_seats = Booking.get_booked_seats(
                journey_date=journey_date_obj, coach=coach, company=company)
            booked_seats = total_seats - remaining_seats
            occupancy = (booked_seats / total_seats) * 100
            seat_occupancy = "{:.1f}".format(occupancy)
            upcoming_schedule = journey_date >= date.today()
            route_parts = RoutePart.objects.filter(coach=coach, company=company)
            journey_date_details = {
                'coach': coach,
                'journey_date': journey_date,
                'total_seats': total_seats,
                'booked_seats': booked_seats,
                'remaining_seats': remaining_seats,
                'seat_occupancy': seat_occupancy,
                'upcoming_schedule': upcoming_schedule,
                'route_parts': route_parts
            }
            coach_details_list.append(journey_date_details)
    # Get the next 5 days including today
    today = date.today()
    next_five_days = [today + timedelta(days=i) for i in range(6)]
    coach_details_list.sort(key=lambda x: x['booked_seats'], reverse=False)
    context = {
        'coach_details_list': coach_details_list,
        'journey_date': journey_date,
        'next_five_days': next_five_days,
        'active_date': journey_date,  # Add active_date to the context
    }
    return render(request, 'hod_template/coach_details_by_date.html', context)

@user_type_required(user_types=[1, 2])
def views_seat(request, bus_number=None, coach_number=None, journey_date=None, route_id=None, start_point=None, end_point=None):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
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
        start_point=start_point_route, end_point=end_point_route,company=company).first()
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
                                          route_part=route_parts, is_booked=True, company=company).values_list('seat_number', flat=True)
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
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
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
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
                ).values_list('seat_number', flat=True)

                print('second route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            elif start_point_priority < route_part_start_point_priority and end_point_priority <= route_part_start_point_priority \
                    and end_point_priority < route_part_end_point_priority:

                print('Third if')
                route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
                ).values_list('seat_number', flat=True)

                print('third route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            # inside the parent route
            elif (start_point_priority <= route_part_start_point_priority and end_point_priority >= route_part_end_point_priority) \
                    or route_part_start_point_priority < start_point_priority < route_part_end_point_priority \
                    or route_part_start_point_priority < end_point_priority < route_part_end_point_priority:

                other_route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=other_route_part, is_booked=True, company=company
                ).values_list('seat_number', flat=True)
                print('other_route_part_booked_seats: ',
                      other_route_part_booked_seats)
                print('----------------------------------------------------------------')

                for seat_number in other_route_part_booked_seats:
                    if seat_number not in booked_seats:
                        booked_seats.append(seat_number)

            else:

                print('nothing matched!!')

                # if start_point_priority < route_part_start_point_priority < end_point_priority and start_point_priority < route_part_end_point_priority < end_point_priority:

    print("Booked Seats Dictionary1:", booked_seats)

    # Now, the special_booked_seats set contains all booked seats for both special and non-special route parts

    route = Route.objects.get(id=route_id)
    print('route_part: ', route.parts.all())

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
    rows_type_1, rows_type_2, rows_type_3 = generate_rowss(
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

    return render(request, 'hod_template/seatview.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    context = {'booking': booking}
    return render(request, 'hod_template/booking_delete.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    context = {'form': form}
    return render(request, 'hod_template/booking_edit.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def feedback_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    feedbacks = feedback.objects.filter(company=company)
    context = {'feedbacks': feedbacks}
    return render(request, 'hod_template/feedback_list.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def feedback_delete(request, feedback_id):
    feedback_obj = get_object_or_404(feedback, id=feedback_id)

    if request.method == 'POST':
        # Handle the POST request to delete the feedback
        feedback_obj.delete()

        return redirect('feedback_list')

    context = {'feedback_obj': feedback_obj}
    return render(request, 'hod_template/feedback_delete.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def get_boarding_points(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    start_district_name = request.GET.get('start_district')
    end_district_name = request.GET.get('end_district')
    intermediate_district_name = request.GET.get('intermediate_district')

    # Retrieve the District objects based on the selected district names
    start_district = get_object_or_404(District, name=start_district_name)
    end_district = get_object_or_404(District, name=end_district_name)
    intermediate_district = get_object_or_404(
        District, name=intermediate_district_name)

    # Get the boarding points for start, intermediate, and end districts
    start_boarding_points = Counter.objects.filter(district=start_district, company=company)
    intermediate_boarding_points = Counter.objects.filter(
        district=intermediate_district, company=company)
    end_boarding_points = Counter.objects.filter(district=end_district, company=company)

    # Create a list to store the sorted boarding points
    sorted_boarding_points = []

    # Add start and intermediate boarding points first
    sorted_boarding_points.extend(start_boarding_points)
    sorted_boarding_points.extend(intermediate_boarding_points)

    # Add end boarding points last
    sorted_boarding_points.extend(end_boarding_points)

    # Serialize the sorted boarding points to a list of names
    boarding_points = [
        boarding_point.name for boarding_point in sorted_boarding_points]

    return JsonResponse({'boarding_points': boarding_points})

@user_type_required(user_types=[1, 2]) 
@login_required
@permission_required('bus.add_route')
def add_route(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    with open('bus/static/json/districts.json', 'r', encoding='utf-8') as district_file:
        districts_data = json.load(district_file)

    districts = [{'district_name': district['name'], 'bus_stops': [bus_stop['name'] for bus_stop in district.get('bus_stops', [])]}
                 for district in districts_data['districts']]

    if request.method == 'POST':
        start_point_name = request.POST['start_point']
        end_point_name = request.POST['end_point']
        distance = float(request.POST['distance'])
        travel_time_str = request.POST.get('travel_time', '')
        boarding_points = request.POST.getlist('boarding_points')
        intermediate_stops = request.POST.getlist('intermediate_stops')

        start_point_district = District.objects.get(name=start_point_name)
        start_point, created_start = BusStop.objects.get_or_create(
            name=start_point_district, company=company)

        end_point_district = District.objects.get(name=end_point_name)
        end_point, created_end = BusStop.objects.get_or_create(
            name=end_point_district, company=company)

        try:
            time_parts = travel_time_str.split(' ')

            if len(time_parts) == 2 and time_parts[1] == 'hour':
                hours, minutes = map(int, time_parts[0].split(':'))
                travel_time = timedelta(hours=hours, minutes=minutes)
            else:
                raise ValueError

        except (ValueError, IndexError):
            messages.error(
                request, 'Invalid travel time format. Use HH:MM hour')
            return redirect('add_route')

        route = Route.objects.create(
            start_point=start_point,
            end_point=end_point,
            distance=distance,
            travel_time=travel_time,
            company=company
        )

        for intermediate_stop_name in intermediate_stops:
            intermediate_stop_district = District.objects.get(
                name=intermediate_stop_name)
            intermediate_stop, created_intermediate = BusStop.objects.get_or_create(
                name=intermediate_stop_district, company=company)
            route.intermediate_stops.add(intermediate_stop)

        for point_name in boarding_points:
            if point_name in Counter.objects.values_list('name', flat=True):
                boarding_point = BoardingPoint.objects.create(
                    route=route,
                    point_name=point_name,
                    company=company
                )
            else:
                messages.error(
                    request, f'Invalid boarding point: {point_name}')
                return redirect('add_route')

        messages.success(request, 'Route added successfully.')
        return redirect('add_route')

    counters = Counter.objects.filter(company=company)

    context = {'districts': districts, 'counters': counters}
    return render(request, 'hod_template/add_route.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
@permission_required('bus.change_route')
def manage_routes(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        routes = Route.objects.filter(
            Q(start_point__icontains=search_query) | Q(
                end_point__icontains=search_query)
        ).order_by('start_point')
    else:
        routes = Route.objects.all()

    return render(request, 'hod_template/manage_routes.html', {'routes': routes})

@user_type_required(user_types=[1, 2]) 
@login_required
@permission_required('bus.change_route')
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    if request.method == 'POST':
        start_point = request.POST.get('start_point')
        end_point = request.POST.get('end_point')
        distance = request.POST.get('distance')
        travel_time_days = int(request.POST.get('travel_time_days', 0))
        travel_time_hours = int(request.POST.get('travel_time_hours', 0))
        travel_time_minutes = int(request.POST.get('travel_time_minutes', 0))

        # Update the model fields
        route.start_point = start_point
        route.end_point = end_point
        route.distance = distance
        route.travel_time = timedelta(
            days=travel_time_days, hours=travel_time_hours, minutes=travel_time_minutes)

        # Save the changes
        route.save()

        messages.success(request, 'Route updated successfully.')
        return redirect('manage_routes')

    return render(request, 'hod_template/edit_route.html', {'route': route})

@user_type_required(user_types=[1, 2]) 
@login_required
@permission_required('bus.delete_route')
def delete_route(request, route_id):
    if request.method == 'POST':
        try:
            route = Route.objects.get(pk=route_id)
            route.delete()
            return JsonResponse({'success': True})
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'user not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@user_type_required(user_types=[1, 2]) 
@login_required
def coach_detail(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    coaches = Coach.objects.filter(company=company)
    date_today = date.today()
    journey_date_history_objects = JourneyDateHistory.objects.filter(
        journey_date__gte=date_today, company=company)
    for schedule in journey_date_history_objects:
        print('Journey date: ', schedule.journey_date)
    # marked_coaches = [coach.id for coach in coaches if coach.is_marked]
    # for coach in coaches:
    #     print('Coach routes:', coach.routes.all())
    # subject = 'welcome to our bus webste'
    # message = 'Hi thank you for registering in our bus website.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['ajayghosh28@gmail.com' ]
    # send_mail( subject, message, email_from, recipient_list )
    if request.method == 'POST':
        marked_coaches = request.POST.getlist('marked_coaches')
        new_journey_date_str = request.POST.get('new_journey_date')
        new_return_date = request.POST.get('new_return_date')
        departure_time = request.POST.get('departure_time')
        changed_coaches = Coach.objects.filter(id__in=marked_coaches, company=company)
        marked_coach_numbers = [str(coach.coachnumber)
                                for coach in changed_coaches]
        print('New journey date: ', new_journey_date_str)
        print('departure time: ', departure_time)
        if new_journey_date_str:
            new_journey_date = datetime.strptime(
                new_journey_date_str, '%Y-%m-%d').date()
            for coach in changed_coaches:
                # coach.journey_dates = coach.journey_dates.add('new_journey_date') if new_journey_date else coach.journey_dates
                # coach.returndate = new_return_date if new_return_date else coach.returndate
                if departure_time:
                    coach.depraturetime = departure_time
                if new_journey_date:
                    journey_date_exist = JourneyDateHistory.objects.filter(
                        journey_date=new_journey_date, company=company).first()
                    print('journey_date_exist: ', journey_date_exist)
                    if not journey_date_exist:
                        print('True')
                        journey_date = JourneyDateHistory.objects.create(
                            company=company,
                            journey_date=new_journey_date)
                        coach.journey_dates.add(journey_date)
                        coach.save()
                    else:
                        print('Date already exists: ')
                        coach.journey_dates.add(journey_date_exist)
                        coach.save()
                else:
                    error_message = 'Server Error'
                    print(error_message)
            marked_coach_numbers_str = ', '.join(marked_coach_numbers)
            messages.success(
                request, f"Journey dates and Return dates updated successfully for coaches: {marked_coach_numbers_str}.")
        elif new_journey_date_str == '':
            messages.error(request, "Please provide a valid journey date.")
        print('marked_coaches: ', marked_coaches)
        redirect('coach_detail')
    context = {'coaches': coaches, 'date_today': date_today}
    # for route in coach.routes.all():
    #     print(route)
    return render(request, 'hod_template/coach_detail.html', context)


@user_type_required(user_types=[1, 2]) 
@login_required
def manage_coach(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    search_query = request.GET.get('search_query', '')

    if search_query:
        coaches = Coach.objects.filter(
            Q(coachmodelname_icontains=search_query) | Q(
                coachnumber_icontains=search_query)
        ).order_by('coachmodelname')
    else:
        coaches = Coach.objects.filter(company=company).order_by('coachmodelname')

    return render(request, 'hod_template/manage_coach.html', {'coaches': coaches, 'search_query': search_query})

@user_type_required(user_types=[1, 2]) 
@login_required
def edit_coach(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)

    if request.method == 'POST':
        # Retrieve the updated data from the form
        coachmodelname = request.POST.get('coachmodelname')
        coachnumber = request.POST.get('coachnumber')
        coachtype = request.POST.get('coachtype')
        arrivaltime = request.POST.get('arrivaltime')
        cancellation_policy = request.POST.get('cancellation_policy')
        facilities = request.POST.get('facilities')
        price = request.POST.get('price')

        # Validate the required fields
        if not coachmodelname or not coachnumber or not coachtype or not arrivaltime or not cancellation_policy or not price:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('edit_coach', coach_id=coach_id)

        # Update the coach object with the new data
        coach.coachmodelname = coachmodelname
        coach.coachnumber = coachnumber
        coach.coachtype = coachtype
        coach.arrivaltime = arrivaltime
        coach.cancellation_policy = cancellation_policy
        coach.facilities = facilities
        coach.price = price
        coach.save()

        messages.success(request, 'Coach updated successfully!')
        return redirect('manage_coach')

    return render(request, 'hod_template/edit_coach.html', {'coach': coach})

@user_type_required(user_types=[1, 2]) 
@login_required
def delete_coach(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)

    if request.method == 'POST':
        # Delete the coach object
        coach.delete()

        messages.success(request, 'Coach deleted successfully!')
        return redirect('manage_coach')

    return render(request, 'hod_template/delete_coach.html', {'coach': coach})

@user_type_required(user_types=[1, 2]) 
def manage_coach_view(request, coach_id):
    coach = Coach.objects.get(id=coach_id)

    if request.method == 'POST':
        journey_date = request.POST.get('journey_date')

        if journey_date:
            try:
                journey_date_obj = datetime.strptime(
                    journey_date, '%Y-%m-%d').date()
                journey_dates = coach.journey_dates.filter(
                    journey_date=journey_date_obj)
            except ValueError:
                journey_dates = coach.journey_dates.all()
        else:
            journey_dates = coach.journey_dates.all()
    else:
        journey_dates = coach.journey_dates.all()

    context = {
        'coach': coach,
        'journey_dates': journey_dates
    }

    return render(request, 'hod_template/manage_coach_view.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def seat_booking_details(request, coach_id, journey_date_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    coach = Coach.objects.get(id=coach_id)
    journey_date = JourneyDateHistory.objects.get(id=journey_date_id)
    seat_bookings = Booking.objects.filter(
        coach=coach, journey_date=journey_date, company=company)

    search_query = request.GET.get('search', '')

    if search_query:
        seat_bookings = seat_bookings.filter(
            Q(id__icontains=search_query) | Q(
                user__username__icontains=search_query)
        )

    context = {
        'coach': coach,
        'journey_date': journey_date,
        'seat_bookings': seat_bookings,
        'search_query': search_query  # Pass the search query to the template
    }

    return render(request, 'hod_template/seat_booking_details.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def update_coach_journey_dates(request):
    if request.method == 'GET':
        try:
            coach_id = request.GET.get('coachId')
            # print('Coach request id: ', coach_id)
            if coach_id:

                upcoming_schedule_list = []
                upcoming_schedule_list_coach = []

                coach = Coach.objects.get(id=coach_id)

                # since JourneyDateHistory and Coach have many to many relationhip, I have to extract it as value_list
                journey_dates = coach.journey_dates.values_list(
                    'journey_date', flat=True)
                # append the auery set in a list
                journey_date_list = list(journey_dates)
                # print('journey_date_list: ', journey_date_list)

                # get all the journey dates from upcoming schedule(greater than or equal to taday's date)
                for upcoming_schedule in journey_date_list:
                    if upcoming_schedule >= date.today():
                        upcoming_schedule_list.append(upcoming_schedule)

                today = date.today()
                # get the dates that are in upcoming schedule and also greater
                upcoming_journey_dates = JourneyDateHistory.objects.filter(
                    Q(journey_date__in=upcoming_schedule_list))
                # upcoming_journey_dates = JourneyDateHistory.objects.filter(Q(journey_date_in=upcoming_schedule_list) & Q(journey_date_gte=today))

                """ since data is passed as a Json object, we have to serialize the query set in to a json format.
                    It returns Json formatted string which is not iterable, so we need to deserialize it using json.loads.
                    Deserialized data is is Json object which is iterable
                """
                upcoming_journey_dates_serialized = serializers.serialize(
                    'json', upcoming_journey_dates)
                upcoming_journey_dates_deserialized = json.loads(
                    upcoming_journey_dates_serialized)

                response_data = {
                    'upcoming_schedule_list_coach': upcoming_journey_dates_deserialized,
                    'coach_id': coach_id,
                    'coach_number': coach.coachnumber
                }

                return JsonResponse(response_data)

        except json.JSONDecodeError:
            pass
    return JsonResponse({'coach_id': None})

@user_type_required(user_types=[1, 2]) 
@login_required
def update_each_journey_date(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        form_data = request.POST
        coach_id = form_data.get('coachId')
        current_date_str = form_data.get('currentDate')

        # Retrieve the field_name from `form_data`. Since the field name dynamic we used `key.startswith`. `next` finds the first match
        field_name = next((key for key in form_data.keys()
                          if key.startswith('new_journey_date-')), None)

        # retrieve the journey_date from the field_name
        journey_date_field = form_data.get(field_name)

        # retrieve the current set for the coach
        if journey_date_field:
            current_date = datetime.strptime(
                current_date_str, '%Y-%m-%d').date()

            # convert the updated journey_date to datetime type
            new_journey_date = datetime.strptime(
                journey_date_field, '%Y-%m-%d').date()

            current_journey_date = JourneyDateHistory.objects.filter(
                journey_date=current_date, company=company).first()

            coach = Coach.objects.get(id=coach_id)
            journey_date = JourneyDateHistory.objects.filter(
                journey_date=new_journey_date, comapny=company).first()

            # coach.journey_dates.set(journey_date)\
            if not journey_date:
                journey_date = JourneyDateHistory.objects.create(
                    journey_date=new_journey_date, company=company)
                coach.journey_dates.remove(current_journey_date)
                coach.journey_dates.add(journey_date)
                # messages.success(request, f"Journey date for coach {coach.coachnumber} is updated from {current_journey_date.journey_date} to {journey_date.journey_date}")
                return JsonResponse({'success': True, 'message': f"Journey date for coach {coach.coachnumber} is updated from {current_journey_date.journey_date} to {journey_date.journey_date}"})

            elif journey_date and current_journey_date:
                coach.journey_dates.remove(current_journey_date)
                coach.journey_dates.add(journey_date)
                # messages.success(request, f"Journey date for coach {coach.coachnumber} is updated from {current_journey_date.journey_date} to {journey_date.journey_date}")
                return JsonResponse({'success': True, 'message': f"Journey date for coach {coach.coachnumber} is updated from {current_journey_date.journey_date} to {journey_date.journey_date}"})

        else:
            # messages.error(request, "Please provide a valid journey date.")
            return JsonResponse({'success': False, 'message': 'Please provide a valid journey date.'})

@user_type_required(user_types=[1, 2]) 
@login_required
def view_coach_details(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'GET':
        try:
            coach_id = request.GET.get('coachId')
            print('Coach request id: ', coach_id)
            if coach_id:

                upcoming_schedule_list = []
                upcoming_schedule_list_coach = []

                coach = Coach.objects.get(id=coach_id)
                coach_details_list = []

                for journey_date in coach.journey_dates.all():
                    booked_seats = Booking.get_booked_seats(
                        journey_date=journey_date, coach=coach, company=company)
                    total_seats, remaining_seats = booked_seats
                    booked_seats = total_seats - remaining_seats
                    occupancy = (booked_seats / total_seats) * 100
                    seat_ocuupancy = "{:.1f}".format(occupancy)

                    if journey_date.journey_date >= date.today():
                        upcoming_schedule = True
                    else:
                        upcoming_schedule = False

                    journey_date_details = {
                        'journey_date': journey_date.journey_date,
                        'total_seats': total_seats,
                        'booked_seats': booked_seats,
                        'remaining_seats': remaining_seats,
                        'seat_ocuupancy': seat_ocuupancy,
                        'upcoming_schedule': upcoming_schedule
                    }

                    coach_details_list.append(journey_date_details)

                response_data = {
                    'coach_details_list': coach_details_list,
                    'coach_id': coach_id,
                    'coach_number': coach.coachnumber
                }

                return JsonResponse(response_data)

        except json.JSONDecodeError:
            pass
    return JsonResponse({'coach_id': None})

@user_type_required(user_types=[1, 2]) 
@login_required
def add_facilities(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'POST':
        # If 'edit_facility_id' is present in POST data, it means we want to edit an existing facility
        edit_facility_id = request.POST.get('edit_facility_id')
        if edit_facility_id:
            facility = get_object_or_404(Facility, id=edit_facility_id)
            facility_name = request.POST.get('facility_name')

            # Update the facility name
            facility.name = facility_name
            facility.save()

            # Add success message
            messages.success(request, 'Facility successfully updated.')
        else:
            # Otherwise, it's a new facility to add
            facility_name = request.POST.get('facility_name')
            Facility.objects.create(name=facility_name,company=company)

            # Add success message
            messages.success(request, 'Facility successfully added.')

        # Redirect to the appropriate page

    # Fetch existing facilities for rendering in the form
    facilities = Facility.objects.filter(company=company)

    return render(request, 'hod_template/add_facilities.html', {
        'facilities': facilities,
    })

@user_type_required(user_types=[1, 2]) 
@login_required
def edit_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    if request.method == 'POST':
        facility_name = request.POST.get('facility_name')
        facility.name = facility_name
        facility.save()
        messages.success(request, 'Facility updated successfully.')
        return redirect('manage_facilities')

    return render(request, 'hod_template/edit_facility.html', {
        'facility': facility,
    })

@user_type_required(user_types=[1, 2]) 
@login_required
def delete_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    facility.delete()
    messages.success(request, 'Facility deleted successfully.')
    return redirect('manage_facilities')

@user_type_required(user_types=[1, 2]) 
@login_required
def manage_facilities(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    search_query = request.GET.get('search_query')
    if search_query:
        facilities = Facility.objects.filter(name__icontains=search_query, company=company)
    else:
        facilities = Facility.objects.filter(company=company)

    return render(request, 'hod_template/manage_facilities.html', {
        'facilities': facilities,
        'search_query': search_query,
    })

@user_type_required(user_types=[1, 2]) 
def search_form(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'GET':
        # Get the search query parameters from the URL
        start_point_name = request.GET.get('start_point')
        end_point_name = request.GET.get('end_point')
        bus_number = request.GET.get('bus_number')
        journey_date_str = request.GET.get('journey_date')

        if journey_date_str:
            try:
                journey_date = datetime.strptime(
                    journey_date_str, '%d-%m-%Y').date()
            except ValueError:
                journey_date = None
        else:
            journey_date = None

        if journey_date is None:
            message = 'Invalid journey date.'
            context = {'message': message}
            return render(request, 'hod_template/ticketbooking.html', context)

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
        journey_dates__journey_date=journey_date,
        company=company
    ).distinct()

    # Filter the RoutePart objects based on the start and end points
    route_parts = RoutePart.objects.filter(
        Q(coach__in=coaches),
        Q(start_point=start_point) & Q(end_point=end_point),
        company=company
    )

    # Get the journey date history associated with the filtered route parts
    journey_date_history = JourneyDateHistory.objects.filter(
        journey_date=journey_date)
    try:
        popup_duration_instance = PopupDuration.objects.first()
        popup_duration_minutes = popup_duration_instance.duration_minutes
    except PopupDuration.DoesNotExist:
        # Handle the case where there are no PopupDuration instances
        popup_duration_minutes = 0
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

        })

    if not bus_data:
        message = 'No buses available for the selected route and date.'
        context = {'message': message}
    else:
        context = {
            'start_point': start_point,
            'end_point': end_point,
            'bus_data': bus_data,
            'journey_date': journey_date,
            # Pass the journey_date variable to the template
            'popup_duration_minutes': popup_duration_minutes
        }

    return render(request, 'hod_template/ticketbooking.html', context)

@user_type_required(user_types=[1, 2]) 
def popup_seat_view_hod(request, bus_number=None, coach_number=None, journey_date=None, route_id=None, start_point=None, end_point=None):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

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
        start_point=start_point_route, end_point=end_point_route, company=company).first()
    print('Route Part Id: ', route_parts.end_point)

    journey_date_coach = coach.journey_dates.first()

    journey_date1 = parse(journey_date).strftime('%Y-%m-%d')
    journey_date_coach = get_object_or_404(
        JourneyDateHistory, journey_date=journey_date1, company=company)

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
                                          route_part=route_parts, is_booked=True, company=company).values_list('seat_number', flat=True)

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
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
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
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
                ).values_list('seat_number', flat=True)

                print('second route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            elif start_point_priority < route_part_start_point_priority and end_point_priority <= route_part_start_point_priority \
                    and end_point_priority < route_part_end_point_priority:

                print('Third if')
                route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=route_parts, is_booked=True, company=company
                ).values_list('seat_number', flat=True)

                print('third route_part_booked_seats: ',
                      route_part_booked_seats)
                print('----------------------------------------------------------------')

            # inside the parent route
            elif (start_point_priority <= route_part_start_point_priority and end_point_priority >= route_part_end_point_priority) \
                    or route_part_start_point_priority < start_point_priority < route_part_end_point_priority \
                    or route_part_start_point_priority < end_point_priority < route_part_end_point_priority:

                other_route_part_booked_seats = Booking.objects.filter(
                    journey_date=journey_date_coach, coach=coach, route_part=other_route_part, is_booked=True, company=company
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
    rows_type_1, rows_type_2, rows_type_3 = generate_rowss(
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

    return render(request, 'hod_template/popupseathod.html', context)

# @user_type_required(user_types=[1, 2]) 
def generate_rowss(seat_type_1, seat_type_2, seat_type_3):
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

# @user_type_required(user_types=[1, 2]) 
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

@user_type_required(user_types=[1, 2])
def booking_hod(request, bus_number, coach_number, journey_date, route_id, route_part_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    # Initialize payment_status with a default value
    payment_status = 'Unpaid'
    amount_paid = 0  # Initialize amount_paid with a default value
    # Get the bus and coach objects
    bus = get_object_or_404(Bus, bus_number=bus_number, company=company)
    coach = get_object_or_404(Coach, bus=bus, coachnumber=coach_number, company=company)
    coach_bus = bus
    # Get active payment methods
    active_payment_methods = PaymentMethod.objects.filter(status=1, company=company)
    active_payment_method_names = [
        method.name for method in active_payment_methods]
    # Parse journey date
    journey_date_str = datetime.strptime(journey_date, '%Y-%m-%d').date()
    journey_dates = JourneyDateHistory.objects.filter(
        journey_date=journey_date_str, company=company).first()
    selected_seat = request.GET.get('seat', '').strip()
    selected_ticket_price = request.GET.get('price', '')
    route_part = get_object_or_404(RoutePart, id=route_part_id, company=company)
    selected_boarding_point_id = request.GET.get('boarding_point', '')
    selected_boarding_point = None
    if selected_boarding_point_id:
        try:
            selected_boarding_point = BoardingPoint.objects.get(
                id=selected_boarding_point_id, company=company)
        except BoardingPoint.DoesNotExist:
            selected_boarding_point = None
    # Generate an 8-digit random PNR
    pnr = str(random.randint(10000000, 99999999))
    tax = Tax.objects.filter(status=1).first()
    tax_value = tax.tax_value
    tax_name = tax.tax_name
    try:
        selected_ticket_price = int(selected_ticket_price)
    except ValueError:
        selected_ticket_price = 0
    tax_amount = math.ceil(selected_ticket_price * (tax_value / 100))
    selected_price = selected_ticket_price + tax_amount
    selected_price = math.ceil(selected_price)
    if request.method == 'POST':
        print('Starting booking_hod view')
# Inside the deduction logic
        if request.user.is_authenticated:
            user = request.user
            email = user.email
        else:
            email = request.POST.get('email', '')
            if not email:
                messages.error(request, 'Please enter your email address')
                return redirect('your_redirect_url_if_email_not_provided')
            try:
                user = Customers.objects.get(email=email)
            except Customers.DoesNotExist:
                user = None
        selected_seat = request.POST.get('selected_seat', '')
        selected_price = request.POST.get('selected_price', '')
        # Inside the deduction logic
        if user.user_type == 2:
            print('User is a counter manager')
            counter = Counter.objects.get(manager=user)
            bank_name = counter.bank_name
            account_name = counter.account_name
            account_no = counter.bank_account_no
            print(f'Current credit balance: {counter.credit_balance}')
            print(f'selected_price: {selected_price}')
            bank = Bank.objects.filter(bank_name=bank_name, account_name=account_name, account_no=account_no).first()
            # Ensure total_cost is a Decimal
            total_cost = Decimal(selected_price)
            if bank:
                if counter.credit_balance >= total_cost:
                    # Deduct the booking cost from the counter manager's credit balance
                    counter.credit_balance -= total_cost
                    counter.save()
                    bank.remaining_balance = counter.credit_balance
                    bank.save()
                    # Create a new Bank object for this counter
                    # # Calculate the difference in the transaction's amount
                    # difference = total_cost
                    # # Print or handle the difference as needed
                    # # Update the counter's credit balance
                    # counter.save()
                else:
                    # If there's insufficient credit balance, raise an exception
                    raise Exception('Insufficient credit balance for booking')
        amount_paid = request.POST.get('amount_paid', 0)
        try:
            amount_paid = Decimal(amount_paid)
        except (ValueError, DecimalException):
            amount_paid = Decimal('0.00')
        customer_mobile = request.POST.get('customer_mobile', '')
        customer_email = request.POST.get('customer_email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        id_type = request.POST.get('id_type', '')
        id_number = request.POST.get('id_number', '')
        address = request.POST.get('address', '')
        country_id = request.POST.get('country_id', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        try:
            validate_email(customer_email)
        except ValidationError:
            messages.error(request, 'Invalid email address')
        customer, created = Customers.objects.get_or_create(email=customer_email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'phone': customer_mobile,
            'id_type': id_type,
            'nid': id_number,
            'address': address,
            'country': country_id,
            'state': state,
            'zip_code': zip_code,
            'company': company
        })
        if not created:
            # If the customer already exists, update their information
            customer.first_name = first_name
            customer.last_name = last_name
            customer.phone = customer_mobile
            customer.id_type = id_type
            customer.nid = id_number
            customer.address = address
            customer.country = country_id
            customer.state = state
            customer.zip_code = zip_code
            customer.company = company
            customer.save()
        if selected_seat and int(selected_price) > 0:
            if Booking.objects.filter(coach=coach, seat_number=selected_seat, journey_date=journey_dates, is_booked=True, company=company).exists():
                messages.error(request, 'Seat already booked.')
            else:
                pnr = str(random.randint(10000000, 99999999))
                selected_payment_method_name = request.POST.get(
                    'selected_payment_method', None)
                selected_payment_method = get_object_or_404(
                    PaymentMethod, name=selected_payment_method_name, company=company)
                created_by = get_user(request)
                booking = Booking.objects.create(
                    user=user,
                    coach=coach,
                    seat_number=selected_seat,
                    route_part=route_part,
                    price=selected_price,
                    is_booked=True,
                    journey_date=journey_dates,
                    pnr=pnr,
                    payment_method=selected_payment_method,
                    customer=customer,
                    route_id=route_id,
                    company=company
                )
                # Create a new Payment instance with the amount_paid
                payment, created = Payment.objects.get_or_create(
                    booking=booking,
                    defaults={
                        'payment_type': selected_payment_method,
                        'amount_paid': amount_paid,  # Use the updated amount_paid variable
                        'payment_status': payment_status,
                        'created_by': created_by,  # Use the updated payment_status variable
                        'company': company, # Use the updated company variable
                    }
                )
                # Update payment_status based on total paid
                total_paid = Payment.objects.filter(booking=booking, company=company).aggregate(
                    Sum('amount_paid'))['amount_paid__sum'] or 0
                # Update payment_status based on total paid
                if total_paid is None or total_paid == 0:
                    payment_status = 'Unpaid'
                elif total_paid == selected_price:
                    payment_status = 'Paid'
                    # Update is_paid field in the Booking model
                    booking.is_paid = True
                elif total_paid > 0:
                    payment_status = 'Partial'
                else:
                    payment_status = 'Unknown'
                # Update payment_status in the Payment model
                payment.payment_status = payment_status
                payment.amount_paid = amount_paid
                payment.save()
                messages.success(request, 'Ticket booking successful.')
                coach_number = coach.coachnumber
                booking_date = booking.journey_date
                booking_seat = booking.seat_number
                ticket_price = booking.price
                ticket_pnr = booking.pnr
                user_name = user.email
                pdf_content = generate_ticket_pdf(str(booking_date), str(coach_number), str(
                    booking_seat), str(ticket_price), str(ticket_pnr), str(user_name))
                pdf_file = ContentFile(pdf_content)
                template_name = 'email_booking.html'
                context = {
                    'user': user.first_name,
                    'coach_number': coach_number,
                    'journey_date': booking_date,
                    'seat_number': booking_seat,
                    'price': ticket_price,
                    'pnr': ticket_pnr,
                    'route_part_id': route_part_id
                }
                html_content = render_to_string(template_name, context)
                mail.send(
                    [user.email],
                    settings.EMAIL_HOST_USER,
                    subject='Booking Successful',
                    html_message=html_content,
                    attachments={'ticket.pdf': pdf_file},
                    priority='now'
                )
        else:
            messages.error(request, 'Invalid seat number or price.')
    booked_seats = Booking.objects.filter(
        coach=coach, company=company).values_list('seat_number', flat=True)
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
        'active_payment_method_names': active_payment_method_names,
        'tax_amount': tax_amount,
        'tax_name': tax_name,
        'payment_status': payment_status,
        'amount_paid': amount_paid,
    }
    return render(request, 'hod_template/boooking_final.html', context)

@user_type_required(user_types=[1, 2]) 
def staff_type_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    search_query = request.GET.get('search_query', '')
    staff_types = StaffType.objects.filter(name__icontains=search_query, company=company)
    context = {
        'staff_types': staff_types,
        'search_query': search_query,
    }
    return render(request, 'hod_template/staff_type_list.html', context)

@user_type_required(user_types=[1, 2]) 
def add_staff_type(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        StaffType.objects.create(name=name,  description=description, company=company)
        return redirect('staff_type_list')
    return render(request, 'hod_template/add_staff_type.html')

@user_type_required(user_types=[1, 2]) 
def edit_staff_type(request, name):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    staff_type = StaffType.objects.get(name=name, company=company)
    if request.method == 'POST':
        staff_type.name = request.POST.get('name')
        staff_type. description = request.POST.get('description')
        staff_type.save()
        return redirect('staff_type_list')
    return render(request, 'hod_template/edit_staff_type.html', {'staff_type': staff_type})

@user_type_required(user_types=[1, 2]) 
def delete_staff_type(request, name):
    staff_type = StaffType.objects.get(name=name)
    if request.method == 'POST':
        staff_type.delete()
        return redirect('staff_type_list')
    return render(request, 'hod_template/delete_staff_type.html', {'staff_type': staff_type})

@user_type_required(user_types=[1, 2]) 
def assign_staff_type(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        staff_type_name = request.POST.get('staff_type')

        try:
            staff = Staffs.objects.get(admin_id=staff_id)
        except Staffs.DoesNotExist:
            messages.error(request, f'Staff with ID {staff_id} not found.')
            return redirect('assign_staff_type')

        try:
            staff_type = StaffType.objects.filter(name=staff_type_name).first()
        except StaffType.DoesNotExist:
            messages.error(
                request, f'Staff type with name {staff_type_name} not found.')
            return redirect('assign_staff_type')

        staff.staff_type = staff_type
        staff.save()

        messages.success(
            request, f'Staff type assigned successfully to {staff.admin.username}.'
        )

    all_staff = Staffs.objects.filter(company=company)
    staff_types = StaffType.objects.filter(company=company)

    return render(request, 'hod_template/assign_staff_type.html', {
        'all_staff': all_staff,
        'staff_types': staff_types,
    })

@user_type_required(user_types=[1, 2]) 
def manage_assigned_staff(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        assigned_staff = Staffs.objects.select_related('admin', 'staff_type').filter(
            Q(admin__username__icontains=search_query) |
            Q(admin__email__icontains=search_query) |
            Q(admin__phone_number__icontains=search_query) |
            Q(staff_type__name__icontains=search_query)
        )
    else:
        assigned_staff = Staffs.objects.select_related('admin', 'staff_type')

    context = {
        'assigned_staff': assigned_staff,
        'search_query': search_query,
    }

    return render(request, 'hod_template/manage_assigned_staff.html', context)

@user_type_required(user_types=[1, 2]) 
def assign_staff_details(request, staff_id):
    staff = get_object_or_404(Staffs, admin_id=staff_id)
    return render(request, 'hod_template/assign_staff_details.html', {'staff': staff})

@user_type_required(user_types=[1, 2]) 
def delete_staff_type(request, staff_id):
    staff = get_object_or_404(Staffs, admin_id=staff_id)

    if request.method == 'POST':
        staff.delete()
        messages.success(
            request, f'Staff {staff.admin.username} deleted successfully.')
        return redirect('manage_assigned_staff')

    return render(request, 'hod_template/delete_staff_assigned.html', {'staff': staff})

@user_type_required(user_types=[1, 2]) 
def add_vehicle(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':

        regi_number = request.POST['regi_number']
        fleet_type = request.POST['fleet_type']
        eng_number = request.POST['eng_number']
        model_name = request.POST['model_name']
        chassis_number = request.POST['chassis_number']
        driver_number = request.POST['driver_number']

        Vehicle.objects.create(
            regi_number=regi_number,
            fleet_type=fleet_type,
            eng_number=eng_number,
            model_name=model_name,
            chassis_number=chassis_number,
            driver_number=driver_number,
            company=company
        )

        messages.success(request, 'Vehicle added successfully.')
        return redirect('vehicle_list')

    return render(request, 'hod_template/add_vehicle.html')

@user_type_required(user_types=[1, 2]) 
def vehicle_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    vehicles = Vehicle.objects.filter(company=company)
    return render(request, 'hod_template/vehicle_list.html', {'vehicles': vehicles})

@user_type_required(user_types=[1, 2]) 
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        # Update the vehicle attributes based on the form data
        vehicle.regi_number = request.POST.get('regi_number')
        vehicle.eng_number = request.POST.get('eng_number')
        vehicle.model_name = request.POST.get('model_name')
        vehicle.chassis_number = request.POST.get('chassis_number')
        vehicle.driver_number = request.POST.get('driver_number')

        vehicle.save()

        return redirect('vehicle_list')

    return render(request, 'hod_template/edit_vehicle.html', {'vehicle': vehicle})

@user_type_required(user_types=[1, 2]) 
def view_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

 
    return render(request, 'hod_template/view_vehicle.html', {'vehicle': vehicle})

@user_type_required(user_types=[1, 2]) 
def delete_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        # Delete the vehicle object
        vehicle.delete()

        return redirect('vehicle_list')

    return render(request, 'hod_template/delete_vehicle.html', {'vehicle': vehicle})

@user_type_required(user_types=[1, 2]) 
def bus_stop_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    bus_stops = BusStop.objects.filter(company=company)
    return render(request, 'hod_template/bus_stop_list.html', {'bus_stops': bus_stops})

@user_type_required(user_types=[1, 2]) 
def add_bus_stop(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        try:
            district_name = request.POST['name']
            district = District.objects.get(name=district_name)

            BusStop.objects.create(name=district, company=company)

            messages.success(request, 'Bus stop added successfully.')
            return redirect('bus_stop_list')

        except District.DoesNotExist:
            messages.error(request, 'Invalid district.')
            return redirect('add_bus_stop')

    districts = District.objects.all()
    context = {'districts': districts}
    return render(request, 'hod_template/add_bus_stop.html', context)

@user_type_required(user_types=[1, 2]) 
def edit_bus_stop(request, pk):
    bus_stop = BusStop.objects.get(pk=pk)
    if request.method == 'POST':
        name = request.POST['name']
        bus_stop.name.name = name
        bus_stop.name.save()
        messages.success(request, 'Bus stop updated successfully.')
        return redirect('bus_stop_list')
    return render(request, 'hod_template/edit_bus_stop.html', {'bus_stop': bus_stop})

@user_type_required(user_types=[1, 2]) 
def delete_bus_stop(request, pk):
    bus_stop = BusStop.objects.get(pk=pk)
    if request.method == 'POST':
        bus_stop.name.delete()
        messages.success(request, 'Bus stop deleted successfully.')
        return redirect('bus_stop_list')
    return render(request, 'hod_template/delete_bus_stop.html', {'bus_stop': bus_stop})

@user_type_required(user_types=[1, 2]) 
def tax_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    taxes = Tax.objects.filter(company=company)
    context = {'taxes': taxes}
    return render(request, 'hod_template/tax_list.html', context)

@user_type_required(user_types=[1, 2]) 
def add_tax(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    if request.method == 'POST':
        try:
            tax_name = request.POST['tax_name']
            tax_value = request.POST['tax_value']
            tax_number = request.POST['tax_number']
            status = request.POST['status']

            Tax.objects.create(
                tax_name=tax_name,
                tax_value=tax_value,
                tax_number=tax_number,
                status=status,
                company=company
            )

            messages.success(request, 'Tax added successfully.')
            return redirect('tax_list')

        except:
            messages.error(request, 'Error adding tax.')
            return redirect('add_tax')

    return render(request, 'hod_template/add_tax.html')

@user_type_required(user_types=[1, 2]) 
def edit_tax(request, tax_id):
    tax = Tax.objects.get(id=tax_id)

    if request.method == 'POST':
        try:
            tax_name = request.POST['tax_name']
            tax_value = request.POST['tax_value']
            tax_number = request.POST['tax_number']
            status = request.POST['status']

            tax.tax_name = tax_name
            tax.tax_value = tax_value
            tax.tax_number = tax_number
            tax.status = status
            tax.save()

            messages.success(request, 'Tax updated successfully.')
            return redirect('tax_list')

        except:
            messages.error(request, 'Error updating tax.')
            return redirect('edit_tax', tax_id=tax_id)

    context = {'tax': tax}
    return render(request, 'hod_template/edit_tax.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_tax(request, tax_id):
    if request.method == 'POST':
        try:
            tax = Tax.objects.get(pk= tax_id)
            tax.delete()
            return JsonResponse({'success': True})
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'user not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@user_type_required(user_types=[1, 2]) 
def payment_method_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    payment_methods = PaymentMethod.objects.filter(company=company)
    context = {'payment_methods': payment_methods}
    return render(request, 'hod_template/payment_method_list.html', context)

@user_type_required(user_types=[1, 2]) 
def add_payment_method(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        name = request.POST['name']
        status = request.POST['status']

        PaymentMethod.objects.create(name=name, status=status, company=company)

        messages.success(request, 'Payment method added successfully.')
        return redirect('payment_method_list')

    return render(request, 'hod_template/add_payment_method.html')

@user_type_required(user_types=[1, 2]) 
def edit_payment_method(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)

    if request.method == 'POST':
        name = request.POST['name']
        status = request.POST['status']

        payment_method.name = name
        payment_method.status = status
        payment_method.save()

        messages.success(request, 'Payment method updated successfully.')
        return redirect('payment_method_list')

    context = {'payment_method': payment_method}
    return render(request, 'hod_template/edit_payment_method.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_payment_method(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)

    if request.method == 'POST':
        payment_method.delete()

        messages.success(request, 'Payment method deleted successfully.')
        return redirect('payment_method_list')

    context = {'payment_method': payment_method}
    return render(request, 'hod_template/delete_payment_method.html', context)

@user_type_required(user_types=[1, 2]) 
@login_required
def user_account_settings(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    try:
        profile = user.profile
    except:
        profile = Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            company=company
        )

    print('profile first name: ', profile.first_name)
    print('profile nid: ', profile.nid)
    print('profile date of birth: ', profile.date_of_birth)

    # attributes = ['last_name', 'mobile_number', 'address', 'nid', 'date_of_birth', 'gender', 'postcode']
    # for attribute in attributes:
    #     if getattr(profile, attribute) is None:
    #         setattr(profile, attribute, '')

    print('profile nid: ', profile.nid)
    print('profile gender: ', profile.gender)

    if request.method == 'POST':

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')

        print('new_password: ', new_password)
        print('confirm_password: ', confirm_password)
        print('username: ', username)
        print('first_name: ', first_name)
        print('last_name: ', last_name)
        print('email: ', email)
        print('birthday: ', birthday)

        if new_password:
            print('has new_pass')
        else:
            print('no new_pass')

        if birthday:
            print('has birthday')
        else:
            print('no birthday')

        if first_name:
            print('has first_name')
        else:
            print('no birthday')

        print('gender: ', gender)

        if new_password and new_password != confirm_password:
            messages.error(request, 'Passwords do not match')

        else:
            if first_name:
                user.username = request.POST.get('username', user.username)
                user.first_name = request.POST.get(
                    'first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.email = request.POST.get('email', user.email)
                user.phone_number = request.POST.get(
                    'phone', user.phone_number)
                profile_picture = request.FILES.get('profile_pic')
                print('no profile picture: ', profile_picture)
                if profile_picture:
                    user.profile_picture = profile_picture
                    print('profile_pic: ', profile_picture)

                if new_password:
                    user.set_password(new_password)

                user.save()

                # this prevents the user to get logged out automatically after updating the password
                update_session_auth_hash(request, user)

                if profile is None:
                    profile = Profile.objects.create(user=user, company=company)

                else:
                    profile.first_name = request.POST.get(
                        'first_name', profile.first_name)
                    profile.last_name = request.POST.get(
                        'last_name', profile.last_name)
                    profile.mobile_number = request.POST.get(
                        'phone', profile.mobile_number)
                    profile.address = request.POST.get(
                        'street_address', profile.address)
                    profile.state = request.POST.get('state', profile.state)
                    profile.postcode = request.POST.get(
                        'zip_code', profile.postcode)
                    profile.nid = request.POST.get(
                        'passport_number', profile.nid)
                    profile.gender = request.POST.get('gender', profile.gender)

                    # if birthday:
                    if birthday:
                        format_to_try = {
                            '%B. %d, %Y',
                            '%b. %d, %Y',
                            '%Y-%m-%d'
                        }

                        for format_str in format_to_try:
                            try:
                                birth_date = datetime.strptime(
                                    birthday, format_str)
                                profile.date_of_birth = birth_date
                                print('birth_date try: ', birth_date)
                                break
                            except:
                                pass

                    else:
                        profile.date_of_birth = None

                    if profile_picture:
                        profile.profile_picture = profile_picture

                    profile.save()
                    messages.success(request, 'Profile Updated Successfully')

            messages.error(request, 'First Name is required')

            return redirect('user_account_settings')

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'hod_template/user_account_settings.html', context)

@user_type_required(user_types=[1, 2]) 
def customer_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    all_customers = Customers.objects.filter(company=company)

    context = {
        'all_customers': all_customers,
    }
    return render(request, 'hod_template/customer_list.html', context)

@user_type_required(user_types=[1, 2]) 
def add_customer(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        # Extract customer data from the form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        id_type = request.POST['id_type']
        nid = request.POST['nid']
        address = request.POST['address']
        # Access the selected country
        country = request.POST.get('country', '')
        state = request.POST['state']
        zip_code = request.POST['zip_code']

        # Get the user associated with the current request
        user = request.user

        # Create the customer record
        customer = Customers.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            id_type=id_type,
            nid=nid,
            address=address,
            country=country,
            state=state,
            zip_code=zip_code,
            company=company
        )

        messages.success(request, 'Customer added successfully.')
        return redirect('customer_list')

    return render(request, 'hod_template/add_customer.html')

@user_type_required(user_types=[1, 2]) 
def edit_customer(request, pk):
    customer = get_object_or_404(Customers, pk=pk)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        id_type = request.POST['id_type']
        nid = request.POST['nid']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        zip_code = request.POST['zip_code']

        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.phone = phone
        customer.id_type = id_type
        customer.nid = nid
        customer.address = address
        customer.country = country
        customer.state = state
        customer.zip_code = zip_code

        customer.save()

        messages.success(request, 'Customer updated successfully.')
        return redirect('customer_list')

    context = {'customer': customer}
    return render(request, 'hod_template/edit_customer.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_customer(request, pk):
    customer = get_object_or_404(Customers, pk=pk)

    if request.method == 'POST':
        customer.delete()

        messages.success(request, 'Customer deleted successfully.')
        return redirect('customer_list')

    context = {'customer': customer}
    return render(request, 'hod_template/delete_customer.html', context)

@user_type_required(user_types=[1, 2]) 
def add_bus_fitness(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    if request.method == 'POST':
        vehicle_id = request.POST['vehicle']
        vehicle = Vehicle.objects.get(id=vehicle_id)

        fitness_name = request.POST['fitness_name']
        fitness_start_date = request.POST['fitness_start_date']
        fitness_end_date = request.POST['fitness_end_date']
        start_mileage = request.POST['start_mileage']
        end_mileage = request.POST['end_mileage']

        BusFitness.objects.create(
            vehicle=vehicle,
            fitness_name=fitness_name,
            fitness_start_date=fitness_start_date,
            fitness_end_date=fitness_end_date,
            start_mileage=start_mileage,
            end_mileage=end_mileage,
            company=company
        )

        return redirect('fitness_list')

    vehicles = Vehicle.objects.filter(company=company)
    context = {'vehicles': vehicles}
    return render(request, 'hod_template/add_bus_fitness.html', context)

@user_type_required(user_types=[1, 2]) 
def fitness_list(request):
    bus_fitness_list = BusFitness.objects.all()
    context = {'bus_fitness_list': bus_fitness_list}
    return render(request, 'hod_template/fitness_list.html', context)

@user_type_required(user_types=[1, 2]) 
def edit_bus_fitness(request, fitness_id):
    bus_fitness = get_object_or_404(BusFitness, id=fitness_id)

    if request.method == 'POST':
        # Update bus_fitness fields based on POST data
        bus_fitness.save()
        return redirect('bus_details_fitness', regi_number=bus_fitness.vehicle.regi_number)

    context = {'bus_fitness': bus_fitness}
    return render(request, 'hod_template/edit_bus_fitness.html', context)

@user_type_required(user_types=[1, 2]) 
def delete_bus_fitness(request, fitness_id):
    bus_fitness = get_object_or_404(BusFitness, id=fitness_id)

    if request.method == 'POST':
        bus_fitness.delete()
        return redirect('bus_details_fitness', regi_number=bus_fitness.vehicle.regi_number)

    context = {'bus_fitness': bus_fitness}
    return render(request, 'hod_template/delete_bus_fitness.html', context)

@user_type_required(user_types=[1, 2]) 
def cancelticket_hod(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)
    # Retrieve all CancelTicket objects
    cancel_tickets = CancelTicket.objects.all()

    # Create a list to store data for display
    cancel_ticket_data = []

    # Iterate through CancelTicket objects and fetch related Booking data
    for cancel_ticket in cancel_tickets:
        booking = cancel_ticket.booking
        coach = booking.coach
        journey_date = booking.journey_date.journey_date
        departure_time = coach.depraturetime
        start_point = booking.route_part.start_point.name.name
        end_point = booking.route_part.end_point.name.name
        payment_status = None
        seat_number = booking.seat_number

        booking_data = {
            'cancel_ticket': cancel_ticket,
            'booking': None,  # Initialize booking_data with None
            'journey_date': None,  # Initialize journey_date with None
            'request_user': None,
            'start_point': start_point,
            'end_point': end_point,
            'seat_number': seat_number,
            'payment_status': payment_status,
            'departure_time': departure_time,
            # Initialize request_user with None
        }

        # Fetch related Booking data
        try:
            booking = Booking.objects.get(id=cancel_ticket.booking.id)
            booking_data['booking'] = booking

            # Fetch journey_date data from Booking
            journey_date = booking.journey_date
            booking_data['journey_date'] = journey_date

            # Fetch the user who requested the cancel ticket
            request_user = booking.user
            booking_data['request_user'] = request_user
        except Booking.DoesNotExist:
            pass

        # Append booking_data to the list
        cancel_ticket_data.append(booking_data)

    # Pass the cancel_ticket_data list to your custom admin template
    context = {'cancel_ticket_data': cancel_ticket_data}
    return render(request, 'hod_template/cancelticket.html', context)

@user_type_required(user_types=[1, 2]) 
def approve_cancel_request(request, cancel_ticket_id):
    try:
        # Retrieve the CancelTicket object to be approved
        cancel_ticket = get_object_or_404(CancelTicket, id=cancel_ticket_id)
        # Check if the CancelTicket status is 'Pending' before approving
        if cancel_ticket.status == 'Pending':
            booking = cancel_ticket.booking
            # Update the status of the booking to indicate it has been canceled
            booking.is_booked = False
            booking.save()
            # Update the status of the cancel ticket to 'Approved'
            cancel_ticket.status = 'Approved'
            cancel_ticket.save()
            messages.success(request, 'Cancel request approved.')
        else:
            messages.error(request, 'This request has already been processed.')
    except CancelTicket.DoesNotExist:
        messages.error(request, 'Cancel request not found.')
    return redirect('cancelticket_hod')

@user_type_required(user_types=[1, 2]) 
def reject_cancel_request(request, cancel_ticket_id):
    try:
        # Retrieve the CancelTicket object to be rejected
        cancel_ticket = get_object_or_404(CancelTicket, id=cancel_ticket_id)
        # Check if the CancelTicket status is 'Pending' before rejecting
        if cancel_ticket.status == 'Pending':
            # Update the CancelTicket status to 'Rejected'
            cancel_ticket.status = 'Rejected'
            cancel_ticket.save()
            messages.success(request, 'Cancel request rejected.')
        else:
            messages.error(request, 'This request has already been processed.')
    except CancelTicket.DoesNotExist:
        messages.error(request, 'Cancel request not found.')
    return redirect('cancelticket_hod')


# def approve_cancel_request(request, cancel_ticket_id):
#     try:
#         # Retrieve the CancelTicket object to be approved
#         cancel_ticket = CancelTicket.objects.get(id=cancel_ticket_id)

#         # Check if the CancelTicket status is 'Pending' before approving
#         if cancel_ticket.status == 'Pending':
#             # Retrieve the associated Booking for this cancel ticket
#             booking = cancel_ticket.booking

#             # Update the CancelTicket status to 'Approved' (save it first)
#             cancel_ticket.status = 'Approved'
#             cancel_ticket.save()

#             # Delete the booking
#             booking.delete()

#             messages.success(request, 'Booking canceled and request approved.')
#         else:
#             messages.error(request, 'This request has already been processed.')

#     except CancelTicket.DoesNotExist:
#         messages.error(request, 'Cancel request not found.')

#     return redirect('hod_template/cancelticket_hod')


# def reject_cancel_request(request, cancel_ticket_id):
#     try:
#         # Retrieve the CancelTicket object to be rejected
#         cancel_ticket = CancelTicket.objects.get(id=cancel_ticket_id)

#         # Check if the CancelTicket status is 'Pending' before rejecting
#         if cancel_ticket.status == 'Pending':
#             # Delete the CancelTicket object
#             cancel_ticket.status = 'Rejected'


#             messages.success(request, 'Cancel request rejected.')
#         else:
#             messages.error(request, 'This request has already been processed.')

#     except CancelTicket.DoesNotExist:
#         messages.error(request, 'Cancel request not found.')

#     return redirect('hod_template/cancelticket_hod')
@user_type_required(user_types=[1, 2]) 
def booking_popup_time(request):
    # Retrieve the PopupDuration object from the database (you may need to specify a filter)
    # You can adjust this query as needed
    popup_duration = PopupDuration.objects.first()
    # Ensure that the duration is in minutes (convert from seconds if necessary)
    if popup_duration:
        duration_minutes = popup_duration.duration_minutes // 60
    else:
        duration_minutes = None
    # Pass the duration_minutes to the template
    context = {'duration_minutes': duration_minutes}
    return render(request, 'hod_template/booking_popup_time.html', context)

@user_type_required(user_types=[1, 2]) 
def set_popup_time(request):
    if request.method == 'POST':
        # Get the new popup time in minutes from the form data (assuming a form field named 'new_duration_minutes')
        new_duration_minutes = request.POST.get('new_duration_minutes')
        # Convert the minutes to seconds
        new_duration_seconds = int(new_duration_minutes) * 60
        # Check if a PopupDuration object exists, and update it if it does, or create it if it doesn't
        popup_duration, created = PopupDuration.objects.get_or_create(
            defaults={'duration_minutes': new_duration_seconds}
        )
        if not created:
            # If the object already exists, update its duration_minutes field
            popup_duration.duration_minutes = new_duration_seconds
            popup_duration.save()
        # Redirect to a success page or to the same page with a success message
        # Replace 'success_page' with the actual URL name or use a different redirection method
    # If it's not a POST request, just render the template with a form to set the popup time
    return render(request, 'hod_template/set_popup_time.html')

@user_type_required(user_types=[1, 2]) 
def all_bookings(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    # Retrieve all bookings ordered by booking date in descending order (most recent first)
    bookings = Booking.objects.filter(company=company).order_by('-booking_date')

    # Create a list to store tuples of booking and its payment status
    booking_status_list = []

    for booking in bookings:
        # Get the latest payment for the booking
        try:
            payment = Payment.objects.filter(
                booking=booking, company=company).latest('date_paid')
            payment_status = payment.payment_status
        except Payment.DoesNotExist:
            # Handle the case where there is no Payment record for the booking
            payment_status = 'No Payment'

        # Append the booking and its payment status as a tuple to the list
        booking_status_list.append((booking, payment_status))

    # Render the template and pass the list of booking_status tuples as context
    context = {'booking_status_list': booking_status_list}
    return render(request, 'hod_template/all_bookings.html', context)

@user_type_required(user_types=[1, 2]) 
def cancel_booking(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    booking = get_object_or_404(Booking, id=booking_id)

    # Retrieve active payment methods
    active_payment_methods = PaymentMethod.objects.filter(status=1, company=company)

    if request.method == 'POST':
        # Set is_booked to False
        booking.is_booked = False

        # Retrieve Cancel Fee, Payment Type, and Payment Details from the form inputs
        cancel_fee = request.POST.get('cancel_fee')
        payment_type = request.POST.get('payment_type')
        payment_details = request.POST.get('payment_details')

        # Save the booking
        booking.save()

        # Create a CancelTicket object and associate it with the booking
        cancel_ticket = CancelTicket.objects.create(
            booking=booking,
            cancel_fee=cancel_fee,
            payment_type=payment_type,
            payment_details=payment_details,
            status='Approved',  # You can set the status as needed
            company=company
        )
        messages.success(request, 'Booking canceled successfully.')

        # Redirect to a suitable URL after cancellation
        # return redirect('your_redirect_url')

    return render(request, 'hod_template/confirmation_template.html', {
        'booking': booking,
        # Pass the active payment methods to the template
        'active_payment_methods': active_payment_methods,
    })
from django.db.models import F

@user_type_required(user_types=[1, 2])
def make_payment(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    # Retrieve the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Retrieve active payment methods
    active_payment_methods = PaymentMethod.objects.filter(status=1, company=company)

    # Calculate the remaining due amount outside the try block
    total_paid = Payment.objects.filter(booking=booking).aggregate(Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')
    remaining_due_amount = max(booking.price - total_paid, Decimal('0.00'))

    if request.method == 'POST':
        try:
            # Process the payment and update the payment status
            payment_type_id = request.POST.get('payment_type')
            amount_paid = request.POST.get('amount_paid')
            payment_details = request.POST.get('payment_details')

            # Check if 'amount_paid' is provided and not empty
            if amount_paid:
                try:
                    amount_paid = Decimal(amount_paid)
                except (TypeError, ValueError):
                    amount_paid = Decimal('0.00')
            else:
                amount_paid = Decimal('0.00')

            # Check if the selected payment_type is active
            selected_payment_type = get_object_or_404(
                PaymentMethod, id=payment_type_id, status=1)

            # Compare and assign the minimum of the two values
            if amount_paid > remaining_due_amount:
                amount_paid = remaining_due_amount

            # Create a Payment instance and save the payment details
            payment = Payment.objects.create(
                booking=booking,
                payment_type=selected_payment_type,
                amount_paid=amount_paid,
                payment_status='Paid' if amount_paid == booking.price else 'Partial',
                created_by=request.user,
                company=company
            )

            # Update the is_paid field in the Booking model
            if payment.payment_status == 'Paid':
                booking.is_paid = True
                booking.save()

            # Add a success message
            messages.success(request, 'Payment successful')

        except Exception as e:
            # Handle any exceptions or errors
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'hod_template/payment_form_template.html', {'booking': booking, 'active_payment_methods': active_payment_methods, 'remaining_due_amount': remaining_due_amount})
@user_type_required(user_types=[1, 2]) 
def view_invoice(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    booking = get_object_or_404(Booking, pk=booking_id)
    user = booking.user
    payment = Payment.objects.filter(booking=booking, company=company).first()
    # Assuming the ticket price is stored in the booking object
    selected_ticket_price = booking.price
    # Fetch the active tax rate (you can modify the filter as needed)
    tax = Tax.objects.filter(status=1, company=company).first()
    if tax:
        tax_value = tax.tax_value
        tax_name = tax.tax_name
        # Calculate tax amount
        tax_amount = math.ceil(selected_ticket_price * (tax_value / 100))
        selected_price = selected_ticket_price + tax_amount
    else:
        # If no tax rate is found, use the price without tax
        selected_price = selected_ticket_price
    # Count the total seats booked by the user
    total_seats_booked_by_user = Booking.objects.filter(user=user, company=company).count()
    # Calculate the total due
    total_due = selected_price - payment.amount_paid
    context = {
        'booking': booking,
        'user': user,
        'payment': payment,
        'tax_amount': tax_amount,  # Include tax amount in the context
        'selected_price': selected_price,
        # Include the final price with tax (or without tax if no tax rate is found)
        'total_due': total_due,
        # Include total seats booked by the user
        'total_seats_booked_by_user': total_seats_booked_by_user,
    }
    return render(request, 'hod_template/invoice_template.html', context)

@user_type_required(user_types=[1, 2]) 
def pos_invoice_view(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    booking = get_object_or_404(Booking, pk=booking_id)
    user = booking.user
    payments = Payment.objects.filter(booking=booking, company=company)

    selected_ticket_price = booking.price


    tax = Tax.objects.filter(status=1, company=company).first()
    
    if tax:
        tax_value = tax.tax_value
        tax_name = tax.tax_name

        tax_amount = math.ceil(selected_ticket_price * (tax_value / 100))
        selected_price = selected_ticket_price + tax_amount
    else:

        selected_price = selected_ticket_price


    total_seats_booked_by_user = Booking.objects.filter(user=user, company=company).count()


    total_due = selected_price - payments.first().amount_paid if payments.exists() else selected_price
    payment_status = payments.first().payment_status if payments.exists() else 'Unpaid'

    context = {
        'booking': booking,
        'user': user,
        'payments': payments,
        'tax_amount': tax_amount,  # Include tax amount in the context
        'selected_price': selected_price,
        'total_due': total_due,
        'total_seats_booked_by_user': total_seats_booked_by_user,
        'payment_status': payment_status,
    }

    # Retrieve booking data based on booking_id
    return render(request, 'hod_template/pos_invoice.html', context)

@user_type_required(user_types=[1, 2]) 
def refund_booking(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    booking = get_object_or_404(Booking, id=booking_id)
    refund = Refund.objects.filter(booking=booking).first()

    # Retrieve active payment methods
    active_payment_methods = PaymentMethod.objects.filter(status=1)

    if request.method == 'POST':
        refund_amount = request.POST.get('refund_amount')
        refund_reason = request.POST.get('refund_reason')
        payment_type = request.POST.get('payment_type')

        partial_payment_amount = request.POST.get('partial_payment_amount')

        if not refund:
            refund = Refund(booking=booking, company=company)

        refund.refund_amount = refund_amount
        refund.refund_reason = refund_reason
        refund.payment_type = payment_type

        refund.partial_payment_amount = partial_payment_amount

        # Check if the refund is approved or not and update the booking accordingly
        if refund.is_approved and not booking.is_paid:
            booking.is_paid = False
            booking.save()
        elif not refund.is_approved and booking.is_paid:
            booking.is_paid = True
            booking.save()

        refund.save()
        # Redirect to a suitable URL after refund request
        # Replace with your actual URL

    return render(request, 'hod_template/refund_form_template.html', {
        'booking': booking,
        'refund': refund,
        'active_payment_methods': active_payment_methods,
    })


logger = logging.getLogger(__name__)

@user_type_required(user_types=[1, 2]) 
def print_ticket_pdf(request, journey_date, coach_number, seat_number, price, pnr, user_name, booking_id):
    # Convert journey_date to a proper date format if needed
    # journey_date = ... (parse it if needed)

    # Retrieve the booking object or return a 404 error if not found
    booking = get_object_or_404(Booking, id=booking_id)

    # Generate the PDF content using the utility function
    pdf_content = generate_ticket_pdf(
        journey_date, coach_number, seat_number, price, pnr, user_name
    )

    # Create a response with PDF content type
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bus_ticket_{booking.pnr}.pdf"'

    return response

@user_type_required(user_types=[1, 2]) 
def payment_details(request, booking_id):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    # Retrieve the Booking object by booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Retrieve the associated payment details for the booking
    payments = Payment.objects.filter(booking=booking, company=company).first()

    context = {
        'booking': booking,
        'payments': payments
    }

    return render(request, 'hod_template/payment_details.html', context)

def approved_cancel_tickets_view(request):
    user = request.user
    company = user.company
    
    # Retrieve approved cancel tickets
    approved_cancel_tickets = CancelTicket.objects.filter(status='Approved', company=company)

    # Prepare a list to store ticket details
    ticket_details = []

    # Iterate through approved cancel tickets
    for cancel_ticket in approved_cancel_tickets:
        # Get the booking associated with the cancel ticket
        booking = cancel_ticket.booking

        # Get the payment associated with the booking
        try:
            payment = Payment.objects.filter(booking=booking, company=company).first()
            payment_details = f"Payment Type: {payment.payment_type}, Amount Paid: {payment.amount_paid}"
        except Payment.DoesNotExist:
            payment_details = "Payment information not available"

        # Create a dictionary with ticket details
        ticket_info = {
            'PNR': booking.pnr,
            'Price': booking.price,
            'Payment Details': payment_details,
            'Date': cancel_ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Append the dictionary to the list
        ticket_details.append(ticket_info)

    # Render the template with the ticket details
    return render(request, 'hod_template/approved_cancel_tickets.html', {'approved_cancel_tickets': approved_cancel_tickets, 'ticket_details': ticket_details})

@user_type_required(user_types=[1, 2]) 
def refund_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    refunds = Refund.objects.filter(company=company).first()
    return render(request, 'hod_template/refund_list_template.html', {'refunds': refunds})


# @login_required
# def create_company(request):
#     # Check if the user is a Root (user_type=0) before allowing company creation
#     if request.user.user_type == 0:
#         if request.method == 'POST':
#             company_name = request.POST.get('company')
#             if company_name:
#                 company = Company.objects.create(
#                     name=company_name, admin=request.user)
#                 return redirect('create_company')
#             else:
#                 error_message = 'Company name is required'
#         else:
#             error_message = None
#     else:
#         error_message = 'Only Root users can create a company.'
#     return render(request, 'hod_template/create_company.html', {'error': error_message})



# @login_required
# def register_user(request, company_id):
#     try:
#         # Get the company based on the company_id parameter
#         company = Company.objects.get(pk=company_id)
#         error_message = None

#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             email = request.POST.get('email')
#             user_type = int(request.POST.get('user_type'))

#             if username and password and email and user_type in [2, 3]:
#                 # Create a new Staff or Users user under the same company
#                 user = CustomUser.objects.create_user(
#                     username=username,
#                     password=password,
#                     email=email,
#                     user_type=user_type
#                 )
#                 # Assign the user to the company
#                 user.company = company
#                 user.save()
#                 return redirect('register_user', company_id=company_id)
#             else:
#                 error_message = 'Username, password, email, and valid user type (2 or 3) are required'
#         else:
#             error_message = None
#     except Company.DoesNotExist:
#         error_message = 'Company not found'

#     return render(request, 'hod_template/register_user.html', {'error': error_message})