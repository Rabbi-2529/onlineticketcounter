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

from django.shortcuts import render, redirect
from django.contrib import messages

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
from inventory.models import *

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
from PIL import Image
from django.views.decorators.http import require_http_methods
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.db.models import F
# Create your views here.
from reportlab.lib import colors
from django.views.decorators.http import require_GET
from django.utils.html import format_html
from dateutil.parser import parse
from django.utils.dateparse import parse_date
from django.core.serializers import serialize


def inventory_home(request):
    return render(request, 'inventory_templates/inventory_home.html')


def add_subcategory(request):
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        parent_category_id = request.POST.get('parent_category')

        if not subcategory_name:
            messages.error(request, 'Subcategory name is required.')
        elif not parent_category_id:
            messages.error(request, 'Parent category is required.')
        else:
            try:
                # Convert parent_category_id to an integer
                parent_category_id = int(parent_category_id)
                parent_category = CategoryItem.objects.get(
                    pk=parent_category_id)
                subcategory = SubCategory(
                    category=parent_category, name=subcategory_name)
                subcategory.save()
                messages.success(request, 'Subcategory added successfully.')
            except (CategoryItem.DoesNotExist, ValueError):
                messages.error(
                    request, 'Invalid parent category. Please select a valid parent category.')

    # Fetch the category choices
    categories = CategoryItem.CATEGORY_CHOICES

    # Fetch all subcategories
    subcategories = SubCategory.objects.all()

    return render(request, 'inventory_templates/add_subcategory.html', {'categories': categories, 'subcategories': subcategories})


# View to list and add brands
def list_and_add_brands(request):
    if request.method == 'POST':
        # Handle brand addition
        name = request.POST.get('name')
        image = request.FILES.get('image')
        if name and image:
            Brand.objects.create(name=name, image=image)
            return redirect('list_brands')

    # Retrieve all brands for listing
    brands = Brand.objects.all()
    return render(request, 'inventory_templates/list_and_add_brands.html', {'brands': brands})


def edit_brand(request, brand_id):
    if request.method == 'POST':
        new_name = request.POST.get('name')
        try:
            brand = get_object_or_404(Brand, pk=brand_id)
            brand.name = new_name
            if 'image' in request.FILES:
                brand.image = request.FILES['image']
            brand.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_brand(request, brand_id):
    if request.method == 'POST':
        try:
            brand = Brand.objects.get(pk=brand_id)
            brand.delete()
            return JsonResponse({'success': True})
        except Brand.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Brand not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# View to list and add units of measurement
def list_and_add_units(request):
    if request.method == 'POST':
        # Handle unit of measurement addition
        name = request.POST.get('name')
        short_name = request.POST.get('short_name')
        if name and short_name:
            UnitOfMeasurement.objects.create(name=name, short_name=short_name)
            return redirect('list_unit')

    # Retrieve all units of measurement for listing
    units = UnitOfMeasurement.objects.all()
    return render(request, 'inventory_templates/list_and_add_units.html', {'units': units})


def edit_unit(request, unit_id):
    if request.method == 'POST':
        data = request.POST  # Assuming you are sending data via a POST request

        try:
            unit = get_object_or_404(UnitOfMeasurement, id=unit_id)
        except Payment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Payment not found.'})

        # Update payment details based on the data received
        unit.name = data.get('new_name', unit.name)
        unit.short_name = data.get('short_name', unit.short_name)

        # Save the updated payment
        unit.save()
        print('unit:', unit)

        return JsonResponse({'success': True, 'message': 'unit updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'This endpoint only supports POST requests for editing payments.'})


def delete_unit(request, unit_id):
    if request.method == 'POST':
        try:
            unit = UnitOfMeasurement.objects.get(pk=unit_id)
            unit.delete()
            return JsonResponse({'success': True})
        except UnitOfMeasurement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Unit of Measurement not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Your other imports and code

def add_item(request):
    if request.method == 'POST':
        # Extract other product data from the request
        product_data = {
            'name': request.POST['name'],
            'category_id': request.POST['category'],
            'expense_id': request.POST.get('expense', None),
            'product_id': request.POST['product_id'],
            'brand_id': request.POST.get('brand', None),
            'warehouse_id': request.POST.get('warehouse', None),
            'barcode': request.POST['barcode'],
            'unit_measurement': request.POST['unit_measurement'],
            'item_price': request.POST['item_price'],
            'tax': request.POST.get('tax', None),
            'discount': request.POST.get('discount', None),
            'stock_alert': request.POST.get('stock_alert', None),
            'purchase_date': request.POST.get('purchase_date', None),
            'purchase_price': request.POST['purchase_price'],
            'last_usage_maintenance_date': request.POST.get('last_usage_maintenance_date', None),
            'condition': request.POST['condition'],
            'responsible_employee': request.POST.get('responsible_employee', ''),

            'price': request.POST.get('price', None),
            'qr_code': request.POST.get('qr_code', ''),
            'barcode': request.POST['barcode'],
        }

        # Check if a product with the same product_id already exists
        existing_product = Product.objects.filter(
            product_id=product_data['product_id']).first()

        if existing_product:
            # Increase the unit_quantity of the existing product
            existing_product.unit_quantity += int(request.POST['unit_quantity'])
            existing_product.save()

            warehouse_id = request.POST.get('warehouse', None)
            if warehouse_id is not None:
                warehouse_id = int(warehouse_id)
                warehouse = Warehouse.objects.get(id=warehouse_id)
                warehouse_product = WarehouseProduct.objects.filter(warehouse=warehouse, product=existing_product).first()

                product_quantity = int(request.POST['unit_quantity'])

                if warehouse_product:
                    # WarehouseProduct already exists, increase the quantity
                    warehouse_product.quantity += 1
                    warehouse_product.save()

                else:
                    # Create a new WarehouseProduct with the specified warehouse
                    WarehouseProduct.objects.create(warehouse=warehouse, product=existing_product, quantity=product_quantity)

            messages.success(request, 'Product quantity updated successfully')
        else:
            # Create a new product instance
            product = Product(**product_data)
            # Set unit_quantity from input
            product.unit_quantity = int(request.POST['unit_quantity'])

            # Handle image upload
            image = request.FILES.get('images')
            if image:
                try:
                    img = Image.open(image)
                    img.verify()

                    # Save the image
                    product.images = image
                except Exception as e:
                    messages.error(request, 'Invalid image file')
            else:
                messages.error(request, 'Image not provided')
            # warehouse_id = request.POST.get('warehouse', None)
            # if warehouse_id:
            #         product.warehouse_id = warehouse_id
            product.save()
            messages.success(request, 'Product added successfully')

        return redirect('product_list')

    # Fetch brands, subcategories, and units for the form
    brands = Brand.objects.all()
    subcategories = SubCategory.objects.all()
    units = UnitOfMeasurement.objects.all()

    # Fetch the list of warehouses
    warehouses = Warehouse.objects.all()

    return render(request, 'inventory_templates/add_item.html', {'brands': brands, 'subcategories': subcategories, 'units': units, 'warehouses': warehouses})


def product_list(request):
    # Fetch a list of products from the database
    products = Product.objects.all()
    brands = Brand.objects.all()

    # Render the products using the 'product_list.html' template
    context = {
        'products': products,
        'brands': brands
    }
    return render(request, 'inventory_templates/product_list.html', context)


def edit_product(request, product_id):
    # Fetch the product based on the provided product_id
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Handle the form submission to update the product
        try:
            # Update the product's attributes with the form data
            product.name = request.POST['name']
            product.category = SubCategory.objects.get(pk=request.POST['category'])
            product.expense = request.POST.get('expense', None)
            product.product_id = request.POST['product_id']
            product.brand = Brand.objects.get(pk=request.POST['brand'])
            product.barcode = request.POST['barcode']
            product.unit_measurement = request.POST['unit_measurement']
            product.item_price = request.POST['item_price']
            product.tax = request.POST.get('tax', None)
            product.discount = request.POST.get('discount', None)
            product.stock_alert = request.POST.get('stock_alert', None)
            product.purchase_date = request.POST.get('purchase_date', None)
            product.purchase_price = request.POST['purchase_price']
            product.last_usage_maintenance_date = request.POST.get('last_usage_maintenance_date', None)
            product.condition = request.POST['condition']
            product.responsible_employee = request.POST.get('responsible_employee', '')
            product.warehouse = request.POST.get('warehouse', None)
            product.price = request.POST.get('price', None)
            product.qr_code = request.POST.get('qr_code', '')
            product.barcode = request.POST['barcode']

            # Save the updated product
            product.save()

            # Return a JSON response indicating success
            response_data = {'success': True, 'message': 'Product updated successfully'}
        except Product.DoesNotExist:
            response_data = {'success': False, 'message': 'Product not found'}
    else:
        response_data = {'success': False, 'message': 'Invalid request method'}

    return JsonResponse(response_data)


def delete_product(request, product_id):
    try:
        # Fetch the product based on the provided product_id and delete it
        product = Product.objects.get(pk=product_id)
        product.delete()
        response_data = {'success': True, 'message': 'Product deleted successfully'}
    except Product.DoesNotExist:
        response_data = {'success': False, 'message': 'Product not found'}

    return JsonResponse(response_data)


def get_adjustment_products_by_warehouse_for_purchase(request, warehouse_id):

    try:
        # Query the products associated with the selected warehouse
        products = Product.objects.filter(warehouse_id=warehouse_id)[:5]

        if products.exists():
            product_data = []

            for product in products:
                subtotal = int(product.item_price) * int(product.unit_quantity)
                product_data.append({
                    'product_id': product.id,
                    'name': product.name,
   
                    'category': str(product.category),
                    'unit_quantity': product.unit_quantity,
                })

                # Update the product's usage count (if applicable)
                product.usage_count = F('usage_count') + 1
                product.save()

            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'No products found for this warehouse'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def get_adjustment_product_details_for_purchase(request):
    try:
        search_query = request.GET.get('search', '')
        # Get distinct products that match the search query
        products = Product.objects.filter(
            Q(product_id__icontains=search_query) | Q(name__icontains=search_query)
        ).distinct()
        print('search query: ', search_query)
        print('searched products: ', products)
        if products.exists():
            # Assuming you want details for the first matching product
            product = products.first()
            # Create a dictionary with product details
            product_data = {
                    'product_id': product.id,
                    'name': product.name,
   
                    'category': str(product.category),
                    'unit_quantity': product.unit_quantity,


            }
            # Update the product's usage count (if applicable)
            product.usage_count = F('usage_count') + 1
            product.save()
            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
def add_inventory_adjustment(request):
    # if request.method == 'POST':
    #     products = Product.objects.all()
    #     for product in products:
    #         adjustment_type = request.POST.get(f'adjustment_type_{product.id}')
    #         quantity = int(request.POST.get(f'quantity_{product.id}', 0))
    #         # Ensure adjustment_type has a value
    #         if adjustment_type is None:
    #             # Handle the case where adjustment_type is not provided
    #             # You might want to add a message or redirect to an error page
    #             # For example:
    #             messages.error(request, 'Adjustment type not provided for a product.')
    #             return redirect('adjustment_list')
    #         # Create an inventory transaction record
    #         transaction = InventoryTransaction(
    #             company=product.company,
    #             user=request.user,
    #             item=product,
    #             quantity=quantity,
    #             transaction_type=adjustment_type,
    #         )
    #         transaction.save()
    #         # Update the product's unit quantity based on the adjustment type
    #         if adjustment_type == 'addition':
    #             product.unit_quantity += quantity
    #         elif adjustment_type == 'subtraction':
    #             product.unit_quantity -= quantity
    #         # Save the updated product
    #         product.save()
    #         # Create an adjustment record
    #         adjustment = Adjustment(
    #             product=product,
    #             quantity=quantity,
    #             adjustment_type=adjustment_type,
    #             warehouse=product.warehouse,  # Include warehouse information
    #         )
    #         adjustment.save()
    #     messages.success(request, 'Inventory adjustments added successfully.')
    #     # Replace 'product_list' with the URL name for your product list view
    #     return redirect('adjustment_list')
    products = Product.objects.all()
    search_product = request.GET.get('search_product', '')
    search_warehouse = request.GET.get('search_warehouse', '')
    search_image = request.GET.get('search_image', '')
    warehouses = Warehouse.objects.all()
    # if search_product:
    #     products = products.filter(product_id__icontains=search_product)
    # if search_warehouse:
    #     products = products.filter(warehouse__icontains=search_warehouse)
    # if search_image:
    #     products = products.filter(image__icontains=search_image)
    return render(request, 'inventory_templates/inventory_adjustment.html', {
        'products': products,
        'search_product': search_product,
        'search_warehouse': search_warehouse,
        'search_image': search_image,
        'warehouses': warehouses
    })
def save_adjustment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data:', data)
        adjustment_date = data['adjustment_date']
        warehouse_id = int(data['source_warehouse'])
        action_type=data['action_type']
        # invoice_number = request.POST.get('invoice_number')
        try:
            product_info = data['product_info']
            try:
                product_ids = [(int(product['product_id']), int(product['quantity'])) for product in product_info]
                try:
                    warehouse = Warehouse.objects.get(id=warehouse_id)
                    for product_id, product_quantity in product_ids:
                       
                       
                            # Get the related objects from their respective models
                            warehouse = Warehouse.objects.get(id=warehouse_id)
                            product = Product.objects.get(id=product_id)
                            # tax = Tax.objects.get(id=tax_id)
                            # discount = Discount.objects.get(id=discount_id)
                            # Create an inventory transaction record
                            transaction = InventoryTransaction(
                                company=product.company,
                                user=request.user,
                                item=product,
                                quantity=product_quantity,
                                
                            )
                            transaction.save()
                            # Update the product's unit quantity based on the adjustment type
                            if action_type == 'Addition':
                                product.unit_quantity += product_quantity
                            elif action_type == 'Subtraction':
                                product.unit_quantity -= product_quantity
                            # Save the updated product
                            product.save()
                            # Create an adjustment record
                            adjustment = Adjustment(
                                product=product,
                                adjustment_date=adjustment_date,
                                quantity=product_quantity,
                                adjustment_type=action_type,
                                warehouse=product.warehouse,  # Include warehouse information
                            )
                            adjustment.save()
                            return JsonResponse({'success': 'Product adjusted successfully'})
                except:
                    return JsonResponse({'error': 'No such warehouse found'})
            except:
                return JsonResponse({'error': 'Product Not found'})
        except:
            return JsonResponse({'error': 'Select Products that you add for purchase'})

def adjustment_list(request):
    adjustment=Adjustment.objects.all()
    return render(request,'inventory_templates/adjustment_list.html',{'adjustment': adjustment})


def view_adjustment(request, adjustment_id):
    try:
        adjustment = Adjustment.objects.get(pk=adjustment_id)
    except Adjustment.DoesNotExist:
        return JsonResponse({'error': 'Adjustment not found'}, status=404)

    adjustment_data = {
        'id': adjustment.id,
        'product_id': adjustment.product.id,
        'quantity': adjustment.quantity,
        'adjustment_type': adjustment.adjustment_type,
        'warehouse': adjustment.warehouse,
      
    }

    return JsonResponse({'adjustment': adjustment_data})


def delete_adjustment(request, adjustment_id):
    if request.method == 'POST':
        try:
            adjustment = Adjustment.objects.get(pk=adjustment_id)
            adjustment.delete()
            return JsonResponse({'success': True})
        except Adjustment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'adjustment not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def add_supplier(request):
    with open('bus/static/json/countries.json') as f:
        country_data = json.load(f)


    if request.method == 'POST':
        # Retrieve supplier details from the POST data
        name = request.POST.get('name')
        supplier_code = request.POST.get('supplier_code')
        address = request.POST.get('address')
        company = request.POST.get('company')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        address_city = request.POST.get('address_city')

        address_postal_code = request.POST.get('address_postal_code')
        address_country = request.POST.get('address_country')
        website = request.POST.get('website')
        payment_history = request.POST.get('payment_history')
        contract_start_date_str = request.POST.get('contract_start_date')
        contract_end_date_str = request.POST.get('contract_end_date')

        # Convert date strings to datetime objects
        try:
            contract_start_date = datetime.strptime(
                contract_start_date_str, '%Y-%m-%d')
        except ValueError:
            contract_start_date = None  # Handle invalid date format gracefully

        try:
            contract_end_date = datetime.strptime(
                contract_end_date_str, '%Y-%m-%d')
        except ValueError:
            contract_end_date = None  # Handle invalid date format gracefully

        # Create and save a new Supplier object
        supplier = Supplier(
            name=name,
            supplier_code=supplier_code,
            address=address,
            company=company,
            phone=phone,
            email=email,

            address_city=address_city,

            address_postal_code=address_postal_code,
            address_country=address_country,
            website=website,
            payment_history=payment_history,
            contract_start_date=contract_start_date,
            contract_end_date=contract_end_date
        )
        supplier.save()

        # Replace 'supplier_list' with the URL name of your supplier list view.
        return redirect('supplier_list')

    return render(request, 'inventory_templates/add_supplier.html',{'country_data':country_data})


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory_templates/supplier_list.html', {'suppliers': suppliers})


def edit_supplier(request, supplier_id):
    response_data = {'success': False, 'message': 'Invalid request method'}
    
    if request.method == 'POST':
        supplier = get_object_or_404(Supplier, pk=supplier_id)

        # Retrieve updated supplier details from the POST data
        name = request.POST.get('name')
        supplier_code = request.POST.get('supplier_code')
        address = request.POST.get('address')
        company = request.POST.get('company')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_city = request.POST.get('address_city')

        # Update the supplier's attributes
        supplier.name = name
        supplier.supplier_code = supplier_code
        supplier.address = address
        supplier.company = company
        supplier.phone = phone
        supplier.email = email
        supplier.address_city = address_city

        # Save the updated supplier
        supplier.save()

        response_data = {'success': True,
                         'message': 'Supplier updated successfully'}

    return JsonResponse(response_data)


def delete_supplier(request, supplier_id):
    try:
        # Fetch the supplier based on the provided supplier_id and delete it
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        response_data = {'success': True,
                         'message': 'Supplier deleted successfully'}
    except Supplier.DoesNotExist:
        response_data = {'success': False, 'message': 'Supplier not found'}

    return JsonResponse(response_data)


def add_biller(request):
    with open('bus/static/json/countries.json') as f:
        country_data = json.load(f)
    if request.method == 'POST':
        # Retrieve biller details from the POST data
        name = request.POST.get('name')
        biller_code = request.POST.get('biller_code')
        address = request.POST.get('address')
        nid = ''.join(request.POST.get(f'nid{i}', '') for i in "0123456789abc")
      
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_country = request.POST.get('address_country')
        address_city = request.POST.get('address_city')
        address_postal_code = request.POST.get('address_postal_code')
   
      
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')
        # Get the selected warehouse ID from the form
        warehouse_id = request.POST.get('warehouse')

        # Create and save a new Biller object with the selected warehouse
        if warehouse_id:
            warehouse = Warehouse.objects.get(pk=warehouse_id)
        else:
            warehouse = None

        biller = Biller(
            name=name,
            biller_code=biller_code,
            address=address,
          
            phone=phone,
            email=email,
            nid=nid,
            address_country=address_country,
            address_city=address_city,
            address_postal_code=address_postal_code,
      
            contract_start_date=contract_start_date,
            contract_end_date=contract_end_date,
            warehouse=warehouse  # Associate the warehouse with the biller
        )
        biller.save()

        # Replace 'biller_list' with the URL name of your biller list view.
        return redirect('biller_list')

    # Fetch the list of available warehouses to populate the dropdown in the form
    warehouses = Warehouse.objects.all()

    return render(request, 'inventory_templates/add_biller.html', {'warehouses': warehouses,'country_data':country_data})


def biller_list(request):
    billers = Biller.objects.all()
    return render(request, 'inventory_templates/biller_list.html', {'billers': billers})


def edit_biller(request, biller_id):
    biller = get_object_or_404(Biller, pk=biller_id)
    if request.method == 'POST':
        try:
            # Retrieve updated biller details from the POST data
            name = request.POST.get('name')
            supplier_code = request.POST.get('supplier_code')
            address = request.POST.get('address')
            manager_name = request.POST.get('manager_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address_country = request.POST.get('address_country')
            address_city = request.POST.get('address_city')
            address_postal_code = request.POST.get('address_postal_code')
            website = request.POST.get('website')
            payment_history = request.POST.get('payment_history')

            # Convert date strings to the "YYYY-MM-DD" format
            contract_start_date_str = request.POST.get('contract_start_date')
            contract_start_date = datetime.strptime(contract_start_date_str, "%b. %d, %Y").strftime("%Y-%m-%d")

            contract_end_date_str = request.POST.get('contract_end_date')
            contract_end_date = datetime.strptime(contract_end_date_str, "%b. %d, %Y").strftime("%Y-%m-%d")

            warehouse_id = request.POST.get('warehouse')
            if warehouse_id:
                warehouse = Warehouse.objects.get(pk=warehouse_id)
            else:
                warehouse = None

            # Update the biller's attributes
            biller.name = name
            biller.supplier_code = supplier_code
            biller.address = address
            biller.manager_name = manager_name
            biller.phone = phone
            biller.email = email
            biller.address_country = address_country
            biller.address_city = address_city
            biller.address_postal_code = address_postal_code
            biller.website = website
            biller.payment_history = payment_history
            biller.contract_start_date = contract_start_date
            biller.contract_end_date = contract_end_date
            biller.warehouse = warehouse

            # Save the updated biller
            biller.save()
            response_data = {'success': True, 'message': 'Biller updated successfully'}
        except Supplier.DoesNotExist:
            response_data = {'success': False, 'message': 'Biller not found'}
        except ValidationError as e:
            response_data = {'success': False, 'message': str(e)}
    else:
        response_data = {'success': False, 'message': 'Invalid request method'}
        warehouses = Warehouse.objects.all()

    return JsonResponse(response_data)

def delete_biller(request, biller_id):
    try:
        # Fetch the supplier based on the provided supplier_id and delete it
        biller = Biller.objects.get(id=biller_id)
        biller.delete()
        response_data = {'success': True,
                         'message': 'Biler deleted successfully'}
    except Supplier.DoesNotExist:
        response_data = {'success': False, 'message': 'Biller not found'}

    return JsonResponse(response_data)


def add_warehouse(request):
    # Load country names and codes from the JSON file
    with open('bus/static/json/countries.json') as f:
        country_data = json.load(f)

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_country = request.POST.get('address_country')
        address_city = request.POST.get('address_city')
        address_postal_code = request.POST.get('address_postal_code')

        warehouse = Warehouse(
            name=name,
            location=location,
            phone=phone,
            email=email,
            address_country=address_country,
            address_city=address_city,
            address_postal_code=address_postal_code
        )
        warehouse.save()

        return redirect('warehouse_list')

    return render(request, 'inventory_templates/add_warehouse.html', {
        'country_data': country_data
    })
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'inventory_templates/warehouse_list.html', {'warehouses': warehouses})


def edit_warehouse(request, warehouse_id):
    response_data = {'success': False, 'message': 'Invalid request method'}
    print('warehouse_id', warehouse_id)

    if request.method == 'POST':
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        # Retrieve updated warehouse details from the POST data
        name = request.POST.get('name')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_country = request.POST.get('address_country')
        address_city = request.POST.get('address_city')
        address_postal_code = request.POST.get('address_postal_code')

        print('warehouse name: ', phone)

        # Update the warehouse's attributes
        warehouse.name = name
        warehouse.location = location
        warehouse.phone = phone
        warehouse.email = email
        warehouse.address_country = address_country
        warehouse.address_city = address_city
        warehouse.address_postal_code = address_postal_code

        # Save the updated warehouse
        warehouse.save()

        response_data = {'success': True,
                         'message': 'Warehouse updated successfully'}

    return JsonResponse(response_data)


def delete_warehouse(request, warehouse_id):
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
        warehouse.delete()
        return JsonResponse({'success': True, 'message': 'Warehouse deleted successfully'})
    except Warehouse.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Warehouse not found'})


selected_products = []


def add_selected_product(request):
    if request.method == 'POST':
        try:
            # Get the selected product and quantity from the POST data
            selected_product_data = json.loads(request.body.decode('utf-8'))
            selected_product_id = selected_product_data.get('id')
            selected_quantity = selected_product_data.get('quantity')

            if not selected_product_id or not selected_quantity:
                raise ValueError('Invalid data for the selected product.')

            selected_quantity = int(selected_quantity)

            # Get the product details based on the selected product ID
            product = Product.objects.get(id=selected_product_id)

            # Create a dictionary with product details
            product_data = {
                'id': product.id,
                'name': product.name,
                'batch_no': product.batch_no,
                'unit': product.unit,
                'price': product.price,
                'quantity': selected_quantity,
                'discount': product.discount,
                'tax': product.tax,
                'sub_total': product.price * selected_quantity - product.discount + product.tax,
            }

            # Add the product data to the selected products list
            selected_products.append(product_data)

            return JsonResponse({'success': True})
        except (ValueError, Product.DoesNotExist) as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def add_transfer(request):
    warehouses = Warehouse.objects.all()
    products = Product.objects.all()
    purcahse_status = Purchase.STATUS_CHOICES

    status_choices = WarehouseTransfer.STATUS_CHOICES
    tax_rate_choices = Tax.TAX_RATE_CHOICES
    return render(request, 'inventory_templates/add_transfer.html', {'warehouses': warehouses, 'products': products, 'status_choices': status_choices, 'tax_rate_choices': tax_rate_choices,'purcahse_status': purcahse_status,})


def save_transfer(request):
    if request.method == 'POST':
        source_warehouse = request.POST.get('source_warehouse')
        destination_warehouse = request.POST.get('destination_warehouse')
        transfer_date = request.POST.get('transfer_date')
        status = request.POST.get('status')
        product_data = json.loads(request.POST.get('json_data'))
        product_info = product_data['product_info']
        tax = request.POST.get('tax_rate')
        discount = request.POST.get('discount')
        shipping_cost = request.POST.get('shipping_cost')
        payment_status = request.POST.get('payment_status')
        # attach_document = data['attach_document']
        staff_remark = request.POST.get('staff_remark')
        payment_note = request.POST.get('payment_note')
        attach_document = request.FILES.get('attach_document')

        source_warehouse = Warehouse.objects.get(id=int(source_warehouse))
        destination_warehouse = Warehouse.objects.get(id=int(destination_warehouse))

        product_ids = [(product['product_id'], int(product['quantity'])) for product in product_info]
        total_quantity = sum([quantity for product_id, quantity in product_ids])
        print('product_ids: ', product_ids)
        print('product_ids: ', len(product_ids))

        transfer = WarehouseTransfer.objects.create(
                source_warehouse=source_warehouse,
                destination_warehouse=destination_warehouse,
                transfer_date=transfer_date,
                status=status,
                tax=tax,
                discount=discount,
                shipping_cost=shipping_cost,
                payment_status=payment_status,
                attach_document=attach_document,
                staff_remark=staff_remark,
                payment_note=payment_note,
                quantity=total_quantity
            )

        for product_id, quantity in product_ids:
            product = Product.objects.get(id=product_id)
            TransferProduct.objects.create(
                product=product,
                transfer = transfer,
                from_warehouse=source_warehouse,
                to_warehouse=destination_warehouse,
                transfer_date=transfer_date,
                quantity=quantity
            )

            
            transfer.products.add(product)
            print('Transfer date: ', transfer_date)

        for transfer_product in transfer.transfered_product.all():
            product = transfer_product.product
            quantity = transfer_product.quantity
            print('product tranfer: ', product)
            print('product quantity: ', quantity)
            source_warehouse = transfer.source_warehouse
            destination_warehouse = transfer.destination_warehouse
            print('source_warehouse: ', source_warehouse)
            get_source_warehouse_product = WarehouseProduct.objects.filter(warehouse=source_warehouse, product=product).first()
            get_destination_warehouse_product = WarehouseProduct.objects.filter(warehouse=destination_warehouse, product=product).first()

            if get_source_warehouse_product is None:
                source_warehouse_product = WarehouseProduct.objects.create(warehouse=source_warehouse, product=product)
                source_warehouse_product.quantity = quantity
                source_warehouse_product.save()
            else:
                get_source_warehouse_product.quantity -= quantity
                get_source_warehouse_product.save()
                print('warehouse_product: ', get_source_warehouse_product.quantity)

            if get_destination_warehouse_product is None:
                destination_warehouse_product = WarehouseProduct.objects.create(warehouse=destination_warehouse, product=product)
                destination_warehouse_product.quantity = quantity
                destination_warehouse_product.save()
            else:
                get_source_warehouse_product.quantity += quantity
                get_source_warehouse_product.save()
                print('warehouse_product: ', get_source_warehouse_product.quantity)

        

    return JsonResponse({'success': True, 'message': 'Transfer has been successfully saved.'})


def get_product_details(request):
    try:
        search_query = request.GET.get('search', '')

        # Get distinct products that match the search query
        products = Product.objects.filter(
            Q(product_id__icontains=search_query) | Q(
                name__icontains=search_query)
        ).distinct()

        if products.exists():
            # Assuming you want details for the first matching product
            product = products.first()

            # Create a dictionary with product details
            product_data = {
                'product_id': product.id,
                'name': product.name,
                # Convert to string for display
                'category': str(product.category),
                # Convert to string for display
                'item_price': str(product.item_price),
                'unit_quantity': product.unit_quantity,
                'tax': str(product.tax),  # Convert to string for display
                # Convert to string for display
                'discount': str(product.discount),
                # Convert to string for display
                'purchase_date': str(product.purchase_date),
                # Convert to string for display
                'purchase_price': str(product.purchase_price),
                # Convert to string for display
                'last_usage_maintenance_date': str(product.last_usage_maintenance_date),
                'condition': product.condition,
            }

            # Update the product's usage count (if applicable)
            product.usage_count = F('usage_count') + 1
            product.save()

            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def add_purchase(request):
    # First define STATUS_CHOICES before referencing it in the context
    purcahse_status = Purchase.STATUS_CHOICES

    warehouses = Warehouse.objects.all()
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    tax_rate_choices = Tax.TAX_RATE_CHOICES
    purchases = Purchase.objects.all()
    for purchase in purchases:
        print('purchase reference: ', purchase.reference_id)
    
    context = {
        'products': products,
        'warehouses': warehouses,
        'suppliers': suppliers,
        'tax_rate_choices': tax_rate_choices,
        'purcahse_status': purcahse_status,
    }

    return render(request, 'inventory_templates/add_purchase.html', context)


def get_products_by_warehouse_for_purchase(request, warehouse_id):
    try:
        # Query the products associated with the selected warehouse
        products = Product.objects.filter(warehouse_id=warehouse_id)[:5]

        if products.exists():
            product_data = []

            for product in products:
                subtotal = int(product.item_price) * int(product.unit_quantity)
                product_data.append({
                    'product_id': product.id,
                    'name': product.name,
                    # Convert to string for display
                    'category': str(product.category),
                    'unit_measurement': product.unit_measurement,
                    # Convert to string for display
                    'item_price': str(product.item_price),
                    'unit_quantity': product.unit_quantity,
                    'tax': str(product.tax),  # Convert to string for display
                    # Convert to string for display
                    'discount': str(product.discount),
                    # Convert to string for display
                    'purchase_date': str(product.purchase_date),
                    # Convert to string for display
                    'purchase_price': str(subtotal),
                    # Convert to string for display
                    'last_usage_maintenance_date': str(product.last_usage_maintenance_date),
                    'condition': product.condition,
                })

                # Update the product's usage count (if applicable)
                product.usage_count = F('usage_count') + 1
                product.save()

            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'No products found for this warehouse'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def get_product_details_for_purchase(request):
    try:
        search_query = request.GET.get('search', '')

        # Get distinct products that match the search query
        products = Product.objects.filter(
            Q(product_id__icontains=search_query) | Q(
                name__icontains=search_query)
        ).distinct()

        print('search query: ', search_query)
        print('searched products: ', products)

        if products.exists():
            # Assuming you want details for the first matching product
            product = products.first()
            subtotal = int(product.item_price) * int(product.unit_quantity)

            # Create a dictionary with product details
            product_data = {
                    'product_id': product.id,
                    'name': product.name,
                    # Convert to string for display
                    'category': str(product.category),
                    'unit_measurement': product.unit_measurement,
                    # Convert to string for display
                    'item_price': str(product.item_price),
                    'unit_quantity': product.unit_quantity,
                    'tax': str(product.tax),  # Convert to string for display
                    # Convert to string for display
                    'discount': str(product.discount),
                    # Convert to string for display
                    'purchase_date': str(product.purchase_date),
                    # Convert to string for display
                    'purchase_price': str(subtotal),
                    # Convert to string for display
                    'last_usage_maintenance_date': str(product.last_usage_maintenance_date),
                    'condition': product.condition,
            }

            # Update the product's usage count (if applicable)
            product.usage_count = F('usage_count') + 1
            product.save()

            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def save_purchase(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        print('data:', data)

        purchase_date = data['transfer_date']
        warehouse_id = int(data['source_warehouse'])
        supplier_id = int(data['supplier'])

        # invoice_number = request.POST.get('invoice_number')
        tax_rate = data['tax_rate']
        discount = data['discount']
        shipping = data['shipping_cost']
        purcahse_status = data['purchase_status']
        purchase_note = data['purchase_note']

        try:
            product_info = data['product_info']

            try:
                product_ids = [(int(product['product_id']), int(product['quantity']), product['subtotal_price']) for product in product_info]

                try:
                    warehouse = Warehouse.objects.get(id=warehouse_id)

                    tax, created_at = Tax.objects.get_or_create(rate=tax_rate)
                    print('tax: ', tax)



                    for product_id, product_quantity, subtotal_price in product_ids:

                    #     # Get the related objects from their respective models
                        warehouse = Warehouse.objects.get(id=warehouse_id)
                        product = Product.objects.get(id=product_id)
                        supplier = Supplier.objects.get(id=supplier_id)
                        # tax = Tax.objects.get(id=tax_id)
                        # discount = Discount.objects.get(id=discount_id)

                        purchase = Purchase.objects.create(
                            purchase_date=purchase_date,
                            warehouse=warehouse,
                            product=product,
                            # invoice_number=invoice_number,
                            order_tax=tax,
                            order_discount=discount,
                            # order_discount=discount,
                            shipping=shipping,
                            quantity=product_quantity,
                            status=purcahse_status,
                            purchase_note=purchase_note,
                            supplier=supplier,
                            grand_total=subtotal_price
                        )

                    return JsonResponse({'success': 'Product purchase saved successfully'})
            
                except:
                    return JsonResponse({'error': 'No such warehouse found'})
                
            except:
                return JsonResponse({'error': 'Product Not found'})
            
        except:
            return JsonResponse({'error': 'Select Products that you add for purchase'})
            

    # # Fetch data for select options
    # warehouses = Warehouse.objects.all()
    # products = Product.objects.all()
    # taxes = Tax.objects.all()
    # discounts = Discount.objects.all()
    # suppliers = Supplier.objects.all()
    # status_choices = Purchase.STATUS_CHOICES

    # return render(request, 'inventory_templates/add_purchase.html', {
    #     'warehouses': warehouses,
    #     'products': products,
    #     'taxes': taxes,
    #     'discounts': discounts,
    #     'suppliers': suppliers,
    #     'status_choices': status_choices
    # })



# def get_products_by_warehouse(request):
#     warehouse_id = request.GET.get('warehouse_id')
#     products = Product.objects.filter(warehouse_id=warehouse_id)[:5]

#     # Prepare the product data to be sent to the client
#     product_data = [
#         {
#                 'name': product.name,
#                 'category': str(product.category),  # Convert to string for display
#                 'item_price': str(product.item_price),  # Convert to string for display
#                 'unit_quantity': product.unit_quantity,
#                 'tax': str(product.tax),  # Convert to string for display
#                 'discount': str(product.discount),  # Convert to string for display
#                 'purchase_date': str(product.purchase_date),  # Convert to string for display
#                 'purchase_price': str(product.purchase_price),  # Convert to string for display
#                 'last_usage_maintenance_date': str(product.last_usage_maintenance_date),  # Convert to string for display
#                 'condition': product.condition,
#         }
#         for product in products
#     ]

#     response_data = {
#         'success': True,
#         'products': product_data,
#     }
#             return JsonResponse({'success': True, 'data': product_data})
#         else:
#             return JsonResponse({'success': False, 'message': 'Product not found'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)})


def get_products_by_warehouse(request, warehouse_id):
    try:
        # Query the products associated with the selected warehouse
        products = Product.objects.filter(warehouse_id=warehouse_id)[:5]

        if products.exists():
            product_data = []

            for product in products:
                product_data.append({
                    'product_id': product.id,
                    'name': product.name,
                    # Convert to string for display
                    'category': str(product.category),
                    # Convert to string for display
                    'item_price': str(product.item_price),
                    'unit_quantity': product.unit_quantity,
                    'tax': str(product.tax),  # Convert to string for display
                    # Convert to string for display
                    'discount': str(product.discount),
                    # Convert to string for display
                    'purchase_date': str(product.purchase_date),
                    # Convert to string for display
                    'purchase_price': str(product.purchase_price),
                    # Convert to string for display
                    'last_usage_maintenance_date': str(product.last_usage_maintenance_date),
                    'condition': product.condition,
                })

                # Update the product's usage count (if applicable)
                product.usage_count = F('usage_count') + 1
                product.save()

            return JsonResponse({'success': True, 'data': product_data})
        else:
            return JsonResponse({'success': False, 'message': 'No products found for this warehouse'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def purchase_list(request):
    # Retrieve a list of purchases from the database
    purchases = Purchase.objects.all()
    payment = Payment.objects.all()
    payment_methods = [  # Define the list of payment method choices
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    ]

    # Retrieve a list of products from the database
    products = Product.objects.all()

    # Retrieve a list of warehouses from the database
    warehouses = Warehouse.objects.all()

    # Retrieve a list of taxes from the database
    taxes = Tax.objects.all()

    # Retrieve a list of discounts from the database
    discounts = Discount.objects.all()

    # Retrieve a list of suppliers from the database
    suppliers = Supplier.objects.all()

    # Iterate through each purchase and calculate payment status and due amount
    for purchase in purchases:
        total_payment = Payment.objects.filter(
            purchase=purchase).aggregate(Sum('amount'))['amount__sum']

        if total_payment is None:
            total_payment = 0  # If no payments exist, set total_payment to 0

        # Determine the status based on the payment amount
        if total_payment == purchase.grand_total:
            purchase.payment_status = 'Paid'
        elif total_payment > 0:
            purchase.payment_status = 'Partial'
        else:
            purchase.payment_status = 'Unpaid'

        # Calculate the due amount
        purchase.due_amount = purchase.grand_total - total_payment

    # Render the HTML template with the list of purchases and products in the context
    return render(request, 'inventory_templates/purchase_list.html', {
        'purchases': purchases,
        'payment_methods': payment_methods,
        'payment': payment,
        'products': products,
        'warehouses': warehouses,
        'taxes': taxes,
        'discounts': discounts,
        'suppliers': suppliers})

@csrf_exempt
def make_payment_inventory(request, purchase_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('purchase id from url: ', purchase_id)
        try:
            purchase = get_object_or_404(Purchase, id=purchase_id)
            print('purchase inventory: ', purchase)
        except Purchase.DoesNotExist:
            return JsonResponse({'error': False, 'message': 'Purchase not found.'})

        # Print all payment data
        print('Payment data received:')
        for key, value in data.items():
            print(f'{key}: {value}')

        payment_date = data.get('payment_date')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        transaction_id = data.get('transaction_id')
        card_number = data.get('card_number', '')
        cheque_number = data.get('cheque_number', '')

        payment = Payment(
            purchase=purchase,
            payment_date=payment_date,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            card_number=card_number,
            cheque_number=cheque_number
        )

        payment.save()
        print('payment:', payment)

        return JsonResponse({'success': True, 'message': 'Payment successfully recorded.'})
    else:
        return JsonResponse({'error': True, 'message': 'Invalid request method.'})

def get_payment_data(request, purchase_id):
    print('purchase id: ', purchase_id)
    if request.method == 'GET':
        # Retrieve the purchase and related payment
        purchase = get_object_or_404(Purchase, id=purchase_id)
        print('purchase: ', purchase)
        # payment = Payment.objects.filter(purchase=purchase).first()
        try:
            payment = Payment.objects.filter(purchase=purchase).first()
            payment_data = {
                'payment_id': payment.id,
                'purchase_id': purchase.id,
                'payment_date': str(payment.payment_date),
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'transaction_id': payment.transaction_id,
            }
        except:
            payment_data = {
                'payment_id': '',
                'purchase_id': '',
                'payment_date': '',
                'amount': '',
                'payment_method': '',
                'transaction_id': ''
            }

        print('paurchase id: ', purchase)

        print('puurchase: ', purchase_id)


        print('payment_date: ', payment_data['payment_date'])
        print('amount: ', payment_data['amount'])
        print('payment_method: ', payment_data['payment_method'])
        print('transaction_id: ', payment_data['transaction_id'])

        return JsonResponse({'success': True, 'payment_data': payment_data})
    else:
        return JsonResponse({'error': False, 'message': 'This endpoint only supports GET requests for viewing payments.'})
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def edit_payment(request, purchase_id):
    try:
        purchase = get_object_or_404(Purchase, id=purchase_id)
        payment = Payment.objects.get(purchase=purchase)
    except Purchase.DoesNotExist:
        return JsonResponse({'error': True, 'message': 'Purchase not found.'})
    except Payment.DoesNotExist:
        return JsonResponse({'error': True, 'message': 'Payment not found for this purchase.'})
    except Exception as e:
        return JsonResponse({'error': True, 'message': str(e)})

    if request.method == 'GET':
        payment_data = {
            'payment_date': str(payment.payment_date),
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'transaction_id': payment.transaction_id,
            'card_number': payment.card_number,
        }
        print('GET request - payment_data:', payment_data)
        return JsonResponse({'success': True, 'payment_data': payment_data}, encoder=DecimalEncoder)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('POST request - received data:', data)  # Debug print
            payment.payment_date = data.get('payment_date', payment.payment_date)
            payment.amount = Decimal(data.get('amount', '0.0'))
            payment.payment_method = data.get('payment_method', payment.payment_method)
            payment.transaction_id = data.get('transaction_id', payment.transaction_id)
            payment.card_number = data.get('card_number', payment.card_number)
            payment.save()

            # Debug prints to check the updated values
            print('POST request - payment successfully updated')  # Debug print
            print('Updated payment_date:', payment.payment_date)
            print('Updated amount:', payment.amount)
            print('Updated payment_method:', payment.payment_method)
            print('Updated transaction_id:', payment.transaction_id)
            print('Updated card_number:', payment.card_number)

            return JsonResponse({'success': True, 'message': 'Payment successfully updated.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': True, 'message': 'Invalid JSON format in request body.'})
        except Exception as e:
            return JsonResponse({'error': True, 'message': str(e)})

    else:
        return JsonResponse({'error': True, 'message': 'This endpoint only supports GET and POST requests.'})
def delete_payment(request, payment_id):

    try:
        # Get the Purchase object or return a 404 response if not found
        payment = get_object_or_404(Payment, id=payment_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the purchase
            payment.delete()
            return JsonResponse({'success': True, 'message': 'Payment deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except Purchase.DoesNotExist:
        # If the purchase doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'Payment not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})


def view_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase_data = serialize_purchase_data(purchase)
    return JsonResponse({'success': True, 'purchase_data': purchase_data})

def serialize_purchase_data(purchase):
    return {
        'purchase_date': str(purchase.purchase_date),
        'warehouse_name': str(purchase.warehouse),
        'product_name': str(purchase.product),
        'invoice_number': purchase.invoice_number,
        'tax_name':  purchase.order_tax.name if purchase.order_tax else '',
        'discount_name': purchase.order_discount.name if purchase.order_discount else '',
        'shipping': str(purchase.shipping),
        'status': purchase.status,
        'purchase_note': purchase.purchase_note,
    }

# def view_purchase(request, custom_id):
#     try:
#         # Retrieve the purchase record to view
#         purchase = Purchase.objects.get(id=custom_id)

#         # Prepare the purchase data
#         purchase_data = {
#             'purchase_date': purchase.purchase_date,
#             'warehouse_name': purchase.warehouse.name,  # Assuming you have a 'name' field in the Warehouse model
#             'product_name': purchase.product.name,  # Assuming you have a 'name' field in the Product model
#             'invoice_number': purchase.invoice_number,
#             'tax_name': purchase.order_tax.name,  # Assuming you have a 'name' field in the Tax model
#             'discount_name': purchase.order_discount.name,  # Assuming you have a 'name' field in the Discount model
#             'shipping': purchase.shipping,
#             'status': purchase.status,
#             'purchase_note': purchase.purchase_note,
#             # Include other purchase attributes as needed
#         }

#         return JsonResponse({'success': True, 'purchase_data': purchase_data})
#     except Purchase.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'Purchase not found'})

# View to edit a purchase record


# def edit_purchase(request, purchase_id):
#     if request.method == 'POST':
#         # Get the purchase object to edit, or return a 404 error if not found
#         purchase = get_object_or_404(Purchase, id=purchase_id)

#         # Retrieve and validate data from the request
#         purchase_date = request.POST.get('purchase_date')
#         warehouse_id = request.POST.get('warehouse')
#         product_id = request.POST.get('product')
#         invoice_number = request.POST.get('invoice_number')
#         tax_id = request.POST.get('tax')
#         discount_id = request.POST.get('discount')
#         shipping = request.POST.get('shipping')
#         status = request.POST.get('status')
#         purchase_note = request.POST.get('purchase_note')
#         grand_total = request.POST.get('grand_total')
#         # Assuming you have a 'supplier' field in your Purchase model
#         supplier_id = request.POST.get('supplier')

#         # Assuming you have models for Warehouse, Product, Tax, Discount, and Supplier
#         warehouse = get_object_or_404(Warehouse, id=warehouse_id)
#         product = get_object_or_404(Product, id=product_id)
#         tax = get_object_or_404(Tax, id=tax_id)
#         discount = get_object_or_404(Discount, id=discount_id)
#         supplier = get_object_or_404(Supplier, id=supplier_id)

#         # Update the fields of the purchase object
#         purchase.purchase_date = purchase_date
#         purchase.warehouse = warehouse
#         purchase.product = product
#         purchase.invoice_number = invoice_number
#         purchase.order_tax = tax
#         purchase.order_discount = discount
#         purchase.shipping = shipping
#         purchase.status = status
#         purchase.purchase_note = purchase_note
#         purchase.grand_total = grand_total
#         purchase.supplier = supplier

#         # Save the changes to the database
#         purchase.save()

#         return JsonResponse({'success': True, 'message': 'Purchase updated successfully'})

#     # Return an error response if the request is not a POST
#     return JsonResponse({'success': False, 'message': 'Invalid request method'})


def edit_purchase(request, purchase_id):
    if request.method == 'GET':
        print('get method hit')
        try:
            purchase = get_object_or_404(Purchase, id=purchase_id)
        except Purchase.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase not found.'})
        taxes = Tax.objects.all()
        taxes_list = json.loads(serialize('json', taxes))
        discount = purchase.order_discount.amount
        for tax in taxes_list:
            print('tax: ', tax['fields']['rate'])
        grand_total = purchase.grand_total
        # Prepare the purchase data for editing
        purchase_data = {
            'purchase_date': purchase.purchase_date,
            'warehouse_id': purchase.warehouse.id,
            'product_id': purchase.product.id,
            'invoice_number': purchase.invoice_number,
            'tax_id': purchase.order_tax.id if purchase.order_tax else None,
            'taxes': taxes_list,
            # 'discount_id': purchase.order_discount.id if purchase.order_discount else None,
            'discount':  discount,
            'shipping': purchase.shipping,
            'status': purchase.status,
            'purchase_note': purchase.purchase_note,
            'grand_total': purchase.grand_total,
            'supplier_id': purchase.supplier.id if purchase.supplier else None,
            'grand_total': grand_total
        }
        return JsonResponse({'success': True, 'purchase_data': purchase_data})
    elif request.method == 'POST':
        data = request.POST
        print('request.POST', request.POST)
        data = json.loads(request.body)
        print('json data: ', data)
        # warehouse_id = request.POST.get('warehouse')
        warehouse_id = data['warehouse']
        product_id = data['product']
        purchase_date = data['purchase_date']
        invoice_number = data['invoice_number']
        order_tax = data['tax']
        order_discount = data['discount']
        shipping = data['shipping']
        status = data['status']
        purchase_note = data['purchase_note']
        grand_total = data['grand_total']
        supplier = data['supplier']
        print('warehouse_id: ', warehouse_id)
        print('product_id: ', product_id)
        print('purchase_date: ', purchase_date)
        print('grand_total: ', grand_total)
        print('supplier: ', supplier)
        try:
            purchase = get_object_or_404(Purchase, id=purchase_id)
        except Purchase.DoesNotExist:
            return JsonResponse({'error': 'Purchase not found'})
        if not warehouse_id:
           return JsonResponse({'error': 'Warehouse not found'})
        if not product_id:
            return JsonResponse({'error': 'Please Specify a Product'})
        if not purchase_date:
            return JsonResponse({'error': 'Date is missing'})
        if not shipping:
            return JsonResponse({'error': 'Shipping cost is missing'})
        if not grand_total:
            return JsonResponse({'error': 'Grand total cost is missing'})
        if not supplier:
            return JsonResponse({'error': 'Supplier is missing'})
        if warehouse_id and product_id and purchase_date and shipping and grand_total and supplier:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            product = Product.objects.get(id=product_id)
            supplier = Supplier.objects.get(id=supplier)
        # Update purchase details based on the data received
            purchase.purchase_date = data.get('purchase_date', purchase.purchase_date)
            purchase.warehouse = warehouse
            purchase.product = product
            purchase.invoice_number = invoice_number
            print('warehouse: ', data.get('warehouse', purchase.warehouse.id))
            if order_tax is not None:
                order_tax = Tax.objects.get(id=order_tax)
                purchase.order_tax = order_tax
            else:
                purchase.order_tax = None
            if order_discount is not None:
                try:
                    discount, created_at = Discount.objects.get_or_create(amount=order_discount)
                except:
                    discount = None
                purchase.order_discount = discount
            else:
                purchase.order_discount = None
            purchase.shipping = shipping
            purchase.status = status
            purchase.purchase_note = purchase_note
            purchase.grand_total = grand_total
            if supplier is not None:
                purchase.supplier = supplier
            else:
                purchase.supplier = None
            # Save the updated purchase
            purchase.save()
            return JsonResponse({'success': True, 'message': 'Purchase updated successfully.'})
        else:
            return JsonResponse({'error': 'Data couldn\'t be updated because of missing values' })
    else:
        return JsonResponse({'error': True, 'message': 'Invalid request method for editing purchases.'})


def delete_purchase(request, purchase_id):
    try:
        # Get the Purchase object or return a 404 response if not found
        purchase = get_object_or_404(Purchase, id=purchase_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the purchase
            purchase.delete()
            return JsonResponse({'success': True, 'message': 'Purchase deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except Purchase.DoesNotExist:
        # If the purchase doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'Purchase not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})


# def delete_purchase(request, purchase_id):
#     try:
#         # Get the Purchase object or return a 404 response if not found
#         purchase = get_object_or_404(Purchase, id=purchase_id)

#         # Check if the request is a POST request (for safety)
#         if request.method == 'POST':
#             # Delete the purchase
#             purchase.delete()
#             return JsonResponse({'success': True, 'message': 'Purchase deleted successfully'})
#         else:
#             # Return a "Method Not Allowed" response for non-POST requests
#             return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
#     except Purchase.DoesNotExist:
#         # If the purchase doesn't exist, return a "Not Found" response
#         return JsonResponse({'success': False, 'message': 'Purchase not found'})
#     except Exception as e:
#         # Handle other exceptions, e.g., database errors
#         return JsonResponse({'success': False, 'message': str(e)})


def create_purchase_return(request):
    if request.method == 'POST':
        # Access POST data and create a new PurchaseReturn instance
        purchase_return_date = request.POST['purchase_return_date']
        reference = request.POST['reference']
        supplier_id = request.POST['supplier']
        warehouse_id = request.POST['warehouse']
        amount = request.POST['amount']
        remark = request.POST['remark']

        # Use request.POST.get to provide a default value for 'action'
        action = request.POST.get('action', 'N/A')

        purchase_id = request.POST['purchase']

        supplier = Supplier.objects.get(pk=supplier_id)
        warehouse = Warehouse.objects.get(pk=warehouse_id)
        purchase = Purchase.objects.get(pk=purchase_id)

        new_purchase_return = PurchaseReturn(
            purchase_return_date=purchase_return_date,
            reference=reference,
            supplier=supplier,
            warehouse=warehouse,
            amount=amount,
            remark=remark,
            action=action,
            purchase=purchase
        )
        new_purchase_return.save()

        return redirect('purchase_return_list')

    suppliers = Supplier.objects.all()
    purchases = Purchase.objects.all()
    warehouses = []  # Initialize an empty list of warehouses
    REMARK_CHOICES = PurchaseReturn.REMARK_CHOICES
    ACTION_CHOICES = PurchaseReturn.ACTION_CHOICES

    return render(request, 'inventory_templates/create_purchase_return.html', {
        'suppliers': suppliers,
        'warehouses': warehouses,
        'purchases': purchases,
        'REMARK_CHOICES': REMARK_CHOICES,
        'ACTION_CHOICES': ACTION_CHOICES
    })


def get_related_warehouses(request, supplier_id):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)

        # Filter purchases based on the selected supplier
        purchases = Purchase.objects.filter(supplier=supplier)

        # Get unique warehouses from the filtered purchases
        warehouse_ids = purchases.values_list(
            'warehouse', flat=True).distinct()
        warehouses = Warehouse.objects.filter(pk__in=warehouse_ids)

        # Prepare data to send as JSON response
        data = [{'id': warehouse.id, 'name': warehouse.name}
                for warehouse in warehouses]
    except Supplier.DoesNotExist:
        data = []  # Supplier not found

    return JsonResponse(data, safe=False)


def get_purchases(request, supplier_id, warehouse_id):
    # Filter Purchase objects based on the supplier and warehouse
    purchases = Purchase.objects.filter(
        supplier_id=supplier_id, warehouse_id=warehouse_id)

    # Create a list of dictionaries containing 'id' and 'name' of each purchase
    data = [{'id': purchase.id, 'name': purchase.product.name}
            for purchase in purchases]

    return JsonResponse(data, safe=False)


def purchase_return_list(request):
    returns = PurchaseReturn.objects.all()
    # Replace with your Supplier model and filtering as needed
    suppliers = Supplier.objects.all()
    # Replace with your Warehouse model and filtering as needed
    warehouses = Warehouse.objects.all()

    return render(request, 'inventory_templates/purchase_return_list.html', {'returns': returns, 'suppliers': suppliers, 'warehouses': warehouses})


def edit_purchase_return(request, return_id):
    if request.method == 'GET':
        try:
            return_instance = get_object_or_404(PurchaseReturn, id=return_id)
        except PurchaseReturn.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase return not found.'})

        # Prepare the purchase return data for editing
        return_data = {
            'return_date': return_instance.return_date,
            'reference': return_instance.reference,
            'warehouse_id': return_instance.warehouse.id if return_instance.warehouse else None,
            'amount': return_instance.amount,
            'remark': return_instance.remark,
            'action': return_instance.action,
            'supplier_id': return_instance.supplier.id if return_instance.supplier else None,
            # Include other purchase return attributes as needed
        }

        return JsonResponse({'success': True, 'purchase_return_data': return_data})

    elif request.method == 'POST':
        data = request.POST

        try:
            return_instance = get_object_or_404(PurchaseReturn, id=return_id)
        except PurchaseReturn.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase return not found.'})

        # Update purchase return details based on the data received
        return_instance.return_date = data.get(
            'return_date', return_instance.return_date)
        return_instance.reference = data.get(
            'reference', return_instance.reference)
        return_instance.amount = data.get('amount', return_instance.amount)
        return_instance.action = data.get('action', return_instance.action)

        if data.get('remark') is not None:
            return_instance.remark = data.get('remark')
        else:
            return_instance.remark = None

        if data.get('warehouse') is not None:
            return_instance.warehouse = data.get('warehouse')
        else:
            return_instance.warehouse = None

        if data.get('supplier') is not None:
            return_instance.supplier = data.get('supplier')
        else:
            return_instance.supplier = None

        # Save the updated purchase return
        return_instance.save()

        return JsonResponse({'success': True, 'message': 'Purchase return updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method for editing purchase returns.'})


def edit_purchase_return(request, return_id):
    if request.method == 'GET':
        try:
            returns = get_object_or_404(PurchaseReturn, id=return_id)
        except PurchaseReturn.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase return not found.'})

        # Prepare the purchase return data for editing
        return_data = {
            'return_date': returns.purchase_return_date,
            'reference': returns.reference,
            'warehouse': returns.warehouse.id if returns.warehouse else None,
            'amount': returns.amount,
            'remark': returns.remark,
            'action': returns.action,
            'supplier': returns.supplier.id if returns.supplier else None,
            # Include other purchase return attributes as needed
        }

        return JsonResponse({'success': True, 'purchase_return_data': return_data})

    elif request.method == 'POST':
        data = request.POST

        try:
            returns = get_object_or_404(PurchaseReturn, id=return_id)
        except PurchaseReturn.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Purchase return not found.'})

        # Update purchase return details based on the data received
        returns.purchase_return_date = data.get(
            'return_date', returns.purchase_return_date)
        returns.reference = data.get(
            'reference', returns.reference)
        returns.amount = data.get('amount', returns.amount)
        returns.remark = data.get('remark', returns.remark)
        returns.action = data.get('action', returns.action)

        # Update supplier and warehouse fields if provided
        returns.supplier = data.get('supplier')
        returns.warehouse = data.get('warehouse')

        # Save the updated purchase return
        returns.save()

        return JsonResponse({'success': True, 'message': 'Purchase return updated successfully.'})

    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method for editing purchase returns.'})


def delete_purchase_return(request, return_id):
    try:
        returns = PurchaseReturn.objects.get(pk=return_id)
        # Delete the Purchase Return
        returns.delete()
        return JsonResponse({'message': 'Purchase Return deleted successfully'})
    except PurchaseReturn.DoesNotExist:
        return JsonResponse({'error': 'Purchase Return not found'}, status=404)


def view_purchase_return_json(request, return_id):
    try:
        returns = PurchaseReturn.objects.get(pk=return_id)
        data = {
            'purchase_return_date': returns.purchase_return_date.strftime('%Y-%m-%d'),
            'reference': returns.reference,
            # Assuming supplier has a 'name' attribute
            'supplier': returns.supplier.name,
            # Assuming warehouse has a 'name' attribute
            'warehouse': returns.warehouse.name,
            'amount': str(returns.amount),
            'remark': returns.remark,
            'action': returns.action,
        }
        return JsonResponse({'success': True, 'purchase_return_data': data})
    except PurchaseReturn.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Purchase Return not found'})


def generate_purchase_report(request):
    report_data = None
    report_title = 'Purchase Report'

    all_purchases = Purchase.objects.all()  # Retrieve all purchases

    if request.method == 'GET' and 'generate_report' in request.GET:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        report_data = Purchase.objects.filter(
            purchase_date__range=[start_date, end_date])

        # Serve the PDF file as a response if 'generate_report' is in the request GET parameters
        pdf_buffer = generate_pdf_report(report_data, report_title)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="purchase_report.pdf"'
        return response

    context = {
        'report_data': report_data,
        'report_title': report_title,
        'all_purchases': all_purchases,
    }

    return render(request, 'inventory_templates/purchase_report_template.html', context)


def generate_pdf_report(report_data, report_title):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add title to the PDF
    elements.append(Paragraph(report_title, styles['Title']))

    if report_data:
        # Create a table for the report data
        # Customize the table headers
        data = [['Product Name', 'Quantity', 'Supplier', 'Warehouse']]

        for purchase in report_data:
            data.append([purchase.product.name, purchase.quantity,
                        purchase.supplier.name, purchase.warehouse.name])

        # Customize the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data, style=table_style)
        elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer


@csrf_exempt
def filter_purchase_report(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        report_data = Purchase.objects.filter(
            purchase_date__range=[start_date, end_date])

        # Serialize the data as JSON and return it as a response
        data = [
            {
                'product': purchase.product.name,
                'quantity': purchase.quantity,
                'supplier': purchase.supplier.name,
                'warehouse': purchase.warehouse.name,
            }
            for purchase in report_data
        ]

        return JsonResponse(data, safe=False)


@csrf_exempt
def generate_payment_report(request):
    report_data = None
    report_title = 'Payment Report'

    all_payments = Payment.objects.select_related(
        'purchase').all()  # Include related Purchase data

    if request.method == 'GET' and 'generate_report' in request.GET:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        report_data = Payment.objects.filter(
            payment_date__range=[start_date, end_date]).select_related('purchase')

        # Serve the PDF file as a response if 'generate_report' is in the request GET parameters
        pdf_buffer = generate_pdf_report_payment(report_data, report_title)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payment_report.pdf"'
        return response

    context = {
        'report_data': report_data,
        'report_title': report_title,
        'all_payments': all_payments,
    }

    return render(request, 'inventory_templates/payment_report_template.html', context)


def generate_pdf_report_payment(report_data, report_title):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add title to the PDF
    elements.append(Paragraph(report_title, styles['Title']))

    if report_data:
        # Create a table for the report data
        # Customize the table headers
        # Customize the table headers
        data = [['Purchase ID', 'Payment Date', 'Amount', 'Payment Method', 'Transaction ID',
                 'Payment Status', 'Purchase Status', 'Warehouse', 'Invoice Number']]

        for payment in report_data:
            data.append([payment.purchase.id, payment.payment_date,
                         payment.amount, payment.get_payment_method_display(), payment.transaction_id])

        # Customize the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data, style=table_style)
        elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer


@csrf_exempt
def filter_payment_report_payment(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        report_data = Payment.objects.filter(
            payment_date__range=[start_date, end_date])

        data = [
            {
                'purchase_id': payment.purchase.id,
                'payment_date': payment.payment_date,
                'amount': payment.amount,
                'payment_method': payment.get_payment_method_display(),
                'transaction_id': payment.transaction_id,
                'payment_status': payment.status,
                'purchase_status': payment.purchase.status,
                'warehouse': payment.purchase.warehouse.name,  # Include warehouse
                'invoice_number': payment.purchase.invoice_number,  # Include invoice_number
            }
            for payment in report_data
        ]

        return JsonResponse(data, safe=False)


@csrf_exempt
def generate_product_report(request):
    report_data = None
    report_title = 'Product Report'
    all_products = Product.objects.all()

    if request.method == 'GET' and 'generate_report' in request.GET:
        warehouse_id = request.GET.get('warehouse_id')
        report_data = Product.objects.filter(warehouse__id=warehouse_id)
        pdf_buffer = generate_pdf_report_product(report_data, report_title)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Product_report.pdf"'
        return response

    context = {
        'report_data': report_data,
        'report_title': report_title,
        'all_products': all_products,
        'all_warehouses': Warehouse.objects.all(),
    }

    return render(request, 'inventory_templates/product_report_template.html', context)

# Your existing product PDF report generation function


def generate_pdf_report_product(report_data, report_title):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(report_title, styles['Title']))

    if report_data:
        data = [['Product Name', 'Category', 'Brand', 'Item Price',
                 'Unit Quantity', 'Tax', 'Discount', 'Stock Alert']]

        for product in report_data:
            data.append([product.name, product.category.name, product.brand.name, product.item_price,
                        product.unit_quantity, product.tax, product.discount, product.stock_alert])

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data, style=table_style)
        elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer

# Your existing product report filtering view


@csrf_exempt
def filter_product_report(request):
    if request.method == 'GET':
        warehouse_id = request.GET.get('warehouse_id')
        report_data = Product.objects.filter(warehouse__id=warehouse_id)

        data = [
            {
                'product_name': product.name,
                'category': product.category.name,
                'brand': product.brand.name,
                'item_price': product.item_price,
                'unit_quantity': product.unit_quantity,
                'tax': product.tax,
                'discount': product.discount,
                'stock_alert': product.stock_alert,
            }
            for product in report_data
        ]

        return JsonResponse(data, safe=False)


@csrf_exempt
def generate_warehouse_report(request):
    report_data = None
    report_title = 'Warehouse Report'

    all_warehouses = Warehouse.objects.all()  # Retrieve all warehouses

    if request.method == 'GET' and 'generate_report' in request.GET:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Convert start_date and end_date from strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter warehouses based on the created_at field
        report_data = Warehouse.objects.filter(
            created_at__range=[start_date, end_date])

        # Serve the PDF file as a response if 'generate_report' is in the request GET parameters
        pdf_buffer = generate_pdf_report_warehouse(report_data, report_title)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="warehouse_report.pdf"'
        return response

    context = {
        'report_data': report_data,
        'report_title': report_title,
        'all_warehouses': all_warehouses,
    }

    return render(request, 'inventory_templates/warehouse_report_template.html', context)


def generate_pdf_report_warehouse(report_data, report_title):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add title to the PDF
    elements.append(Paragraph(report_title, styles['Title']))

    if report_data:
        # Create a table for the report data
        # Customize the table headers
        data = [['Warehouse Name', 'Location', 'Phone', 'Email',
                 'Country', 'City', 'Postal Code', 'Created At']]

        for warehouse in report_data:
            data.append([warehouse.name, warehouse.location, warehouse.phone, warehouse.email,
                         warehouse.address_country, warehouse.address_city, warehouse.address_postal_code, warehouse.created_at])

        # Customize the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data, style=table_style)
        elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer


@csrf_exempt
def filter_warehouse_report(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        report_data = Warehouse.objects.filter(
            created_at__range=[start_date, end_date])

        # Serialize the data as JSON and return it as a response
        data = [
            {
                'name': warehouse.name,
                'location': warehouse.location,
                'phone': warehouse.phone,
                'email': warehouse.email,
                'address_country': warehouse.address_country,
                'address_city': warehouse.address_city,
                'address_postal_code': warehouse.address_postal_code,
                'created_at': warehouse.created_at,
            }
            for warehouse in report_data
        ]

        return JsonResponse(data, safe=False)


def generate_supplier_report(request):
    report_data = None
    report_title = 'Supplier Report'

    all_suppliers = Supplier.objects.all()  # Retrieve all suppliers

    if request.method == 'GET' and 'generate_report' in request.GET:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Convert start_date and end_date from strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter suppliers based on the created_at field
        report_data = Supplier.objects.filter(
            created_at__range=[start_date, end_date])

        # Serve the PDF file as a response if 'generate_report' is in the request GET parameters
        pdf_buffer = generate_pdf_report_supplier(report_data, report_title)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="supplier_report.pdf"'
        return response

    context = {
        'report_data': report_data,
        'report_title': report_title,
        'all_suppliers': all_suppliers,
    }

    return render(request, 'inventory_templates/supplier_report_template.html', context)

# Create a function to generate the PDF report for suppliers


def generate_pdf_report_supplier(report_data, report_title):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Add title to the PDF
    elements.append(Paragraph(report_title, styles['Title']))

    if report_data:
        # Create a table for the report data
        # Customize the table headers
        data = [
            ['Supplier Name', 'Supplier Code', 'Address', 'Company', 'Phone', 'Email', 'Address Street',
             'Address City', 'Address State', 'Address Postal Code', 'Address Country', 'Website', 'Payment History',
             'Contract Start Date', 'Contract End Date', 'Created At']]

        for supplier in report_data:
            data.append([supplier.name, supplier.supplier_code, supplier.address, supplier.company,
                         supplier.phone, supplier.email, supplier.address_street, supplier.address_city,
                         supplier.address_state, supplier.address_postal_code, supplier.address_country,
                         supplier.website, supplier.payment_history, supplier.contract_start_date,
                         supplier.contract_end_date, supplier.created_at])

        # Customize the table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table = Table(data, style=table_style)
        elements.append(table)

    doc.build(elements)
    pdf_buffer.seek(0)

    return pdf_buffer

# Create a function to filter and return JSON data for suppliers (if needed)


def filter_supplier_report(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Convert start_date and end_date from strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter suppliers based on the created_at field
        report_data = Supplier.objects.filter(
            created_at__range=[start_date, end_date])

        # Serialize the data as JSON and return it as a response
        data = [
            {
                'name': supplier.name,
                'supplier_code': supplier.supplier_code,
                'address': supplier.address,
                'company': supplier.company,
                'phone': supplier.phone,
                'email': supplier.email,
                'address_street': supplier.address_street,
                'address_city': supplier.address_city,
                'address_state': supplier.address_state,
                'address_postal_code': supplier.address_postal_code,
                'address_country': supplier.address_country,
                'website': supplier.website,
                'payment_history': supplier.payment_history,
                'contract_start_date': supplier.contract_start_date,
                'contract_end_date': supplier.contract_end_date,
                'created_at': supplier.created_at,
            }
            for supplier in report_data
        ]

        return JsonResponse(data, safe=False)
    


def transferlist(request):
    transfer= WarehouseTransfer.objects.all()
    purchases = Purchase.objects.all()
    return render(request, 'inventory_templates/warehouse_transfer_list.html', {'transfer': transfer,'purchases':purchases})





def stock_report(request):
    used_products = ProductInstallation.objects.all()
    purchase = Purchase.objects.all()
    for pur in purchase:
        print(pur.usedproduct_set)
    stock_products = []
    for product in purchase:
        stock_info = {
            'purchase_date': product.product.purchase_date,
            'product_name': product.product.name,
            'purchase_price': product.product.purchase_price,
            'warehouse': product.warehouse,
            'unit_measurement': product.product.unit_measurement,
            'condition': product.product.condition,
            'available_quantity': product.in_stock_quantity
        }
        stock_products.append(stock_info)
    
    context = {
        'stock_products': stock_products
    }

    return render(request, 'inventory_templates/stock_report.html', context)


def product_installation(request):
    warehouses = Warehouse.objects.all()
    products = Product.objects.all()

    status_choices = WarehouseTransfer.STATUS_CHOICES
    tax_rate_choices = Tax.TAX_RATE_CHOICES
    buses = Bus.objects.all()
    print('buses: ', buses)

    context = {
        'warehouses': warehouses,
        'products': products,
        'status_choices': status_choices,
        'buses': buses,
        'tax_rate_choices': tax_rate_choices
    }

    return render(request, 'inventory_templates/product_installation.html', context)


def save_product_installation(request):
    if request.method == 'POST':
        source_warehouse = request.POST.get('source_warehouse')
        installation_date = request.POST.get('transfer_date')
        bus_id = request.POST.get('bus')
        product_data = json.loads(request.POST.get('json_data'))
        product_info = product_data['product_info']
        installtion_cost = request.POST.get('installation_cost')
        # payment_status = request.POST.get('payment_status')
        # attach_document = data['attach_document']
        staff_remark = request.POST.get('staff_remark')
        purchase_status = request.POST.get('purchase_status')
        installation_note = request.POST.get('installation_note')
        # attach_document = request.FILES.get('attach_document')

        print('product_data: ', product_data)
        print('product_info: ', product_info)

        try:
            bus = Bus.objects.get(id=bus_id)
        except:
            bus = None

        if bus is not None:
            if source_warehouse:
                source_warehouse = Warehouse.objects.get(id=int(source_warehouse))

                products = [(int(product['product_id']), int(product['quantity'])) for product in product_info]

                for product_id, quantity in products:
                    product = Product.objects.filter(id=product_id, warehouse=source_warehouse).first()
                    
                    if product is not None:
                        product_installation = ProductInstallation.objects.create(
                            installation_date=installation_date,
                            warehouse=source_warehouse,
                            product=product,
                            bus=bus,
                            quantity=quantity,
                            purchase_status=purchase_status,
                        )
                        if installation_note != '':
                            product_installation.installation_note = installation_note
                            product_installation.save()

                        warehouse_product = WarehouseProduct.objects.filter(warehouse=source_warehouse, product=product).first()
                        warehouse_product.quantity -= int(quantity)
                        warehouse_product.save()

            return JsonResponse({'success': 'Product Installation information saved successfully.'})


def products_usage_list(request):

    return render(request, 'inventory_templates/products_usage_list.html')


def purchase_invoice(request):
    warehouses = Warehouse.objects.all()
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    tax_rate_choices = Tax.TAX_RATE_CHOICES
    
    context = {
        'products': products,
        'warehouses': warehouses,
        'products': products,
        'suppliers': suppliers,
        'tax_rate_choices': tax_rate_choices
    }

    status_choices = WarehouseTransfer.STATUS_CHOICES
    tax_rate_choices = Tax.TAX_RATE_CHOICES
    return render(request, 'inventory_templates/purchase_invoice.html', context)


def save_purchase_invoice(request):
    if request.method == 'POST':
        warehouse_id = request.POST.get('source_warehouse')
        purchase_date = request.POST.get('transfer_date')
        supplier_id = request.POST.get('supplier')
        product_data = json.loads(request.POST.get('json_data'))
        product_info = product_data['product_info']
        status = request.POST.get('purchase_status')
        # payment_status = request.POST.get('payment_status')
        # attach_document = data['attach_document']
        purchase_note = request.POST.get('purchase_note')
        order_tax = request.POST.get('tax_rate')
        order_discount = request.POST.get('discount')
        shipping = request.POST.get('shipping_cost')
        # attach_document = request.FILES.get('attach_document')

        print('product_data: ', product_data)
        print('product_info: ', product_info)

        tax, created_at = Tax.objects.get_or_create(rate=order_tax)
        print('tax: ', tax)

        discount, created_at = Discount.objects.get_or_create(amount=int(order_discount))

        if warehouse_id and purchase_date and supplier_id:
            source_warehouse = Warehouse.objects.get(id=int(warehouse_id))
            supplier = Supplier.objects.get(id=int(supplier_id))
            products = [(int(product['product_id']), int(product['quantity'])) for product in product_info]

            for product_id, quantity in products:
                product = Product.objects.filter(id=product_id, warehouse=source_warehouse).first()
                purchase = Purchase.objects.filter(product=product).first()

                if purchase is not None:
                    if product is not None:
                        purchase_invoice = PurchaseInvoice.objects.create(
                            invoice_date=purchase_date,
                            warehouse=source_warehouse,
                            purchase=purchase,
                            supplier=supplier,
                            order_tax=tax,
                            order_discount=discount,
                            shipping=shipping,
                            status=status
                        )
                        if purchase_note != '':
                            purchase_invoice.purchase_note = purchase_note
                            purchase_invoice.save()
                    
                    else:
                        print('Product not found')
                        return JsonResponse({'product_error': 'Product not found'}, status=404)

                else:
                    print('Purchase not found')
                    return JsonResponse({'purchase_error': 'Purchase not found'}, status=404)

            return JsonResponse({'success': 'Transfer has been successfully saved.'})
        
        else:
            return JsonResponse({'warehouse_error': 'Please provide all the requred information'})

        
def add_subcategory_expense(request):
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        parent_category_id = request.POST.get('parent_category')

        if not subcategory_name:
            messages.error(request, 'Subcategory name is required.')
        elif not parent_category_id:
            messages.error(request, 'Parent category is required.')
        else:
            try:
                # Convert parent_category_id to an integer
                parent_category_id = int(parent_category_id)
                parent_category = ExpenseCategory.objects.get(
                    pk=parent_category_id)
                subcategory = ExpenseSubCategory(
                    category=parent_category, name=subcategory_name)
                subcategory.save()
                messages.success(request, 'Subcategory added successfully.')
            except (ExpenseCategory.DoesNotExist, ValueError):
                messages.error(
                    request, 'Invalid parent category. Please select a valid parent category.')

    # Fetch the category choices
    categories_expense = ExpenseCategory.EXPENSE_CATEGORY_CHOICES

    # Fetch all subcategories
    subcategories_expense = ExpenseSubCategory.objects.all()

    return render(request, 'inventory_templates/add_subcategory_expense.html', {'categories_expense': categories_expense, 'subcategories_expense': subcategories_expense})



def add_expense(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        warehouse_id = request.POST.get('warehouse')
        expense_category = request.POST.get('expense_category')  # Change here
        sub_category_id = request.POST.get('category')  # Change here
        voucher_no = request.POST.get('voucher_no')
        amount = request.POST.get('amount')
        purchase_note = request.POST.get('purchase_note')
        print(f"date: {date}, warehouse_id: {warehouse_id}, expense_category: {expense_category}, amount: {amount}")

        if not date or not warehouse_id or not expense_category or not amount:
            messages.error(request, 'Date, Warehouse, Expense Type, and Amount are required fields.')
        else:
            try:
                warehouse = Warehouse.objects.get(id=warehouse_id)
                sub_category = None
                if sub_category_id:
                    sub_category = ExpenseSubCategory.objects.get(id=sub_category_id)
                expense = Expense(
                    date=date,
                    warehouse=warehouse,
                    expense_type=expense_category,
                    sub_category=sub_category,
                    voucher_no=voucher_no,
                    amount=amount,
                    purchase_note=purchase_note,
                    expense_category=expense_category,
                )
                expense.save()
                messages.success(request, 'Expense added successfully.')
                return redirect('expense_list')
            except (Warehouse.DoesNotExist, ExpenseSubCategory.DoesNotExist):
                messages.error(request, 'Invalid Warehouse or Subcategory. Please select valid options.')

    subcategory = ExpenseSubCategory.objects.all()
    warehouse = Warehouse.objects.all()

    return render(request, 'inventory_templates/add_expense.html', {'subcategory': subcategory, 'warehouse': warehouse})



def expense_list(request):
    # Retrieve a list of purchases from the database
    expenses = Expense.objects.all()
    payment = Payment.objects.all()
    payment_methods = [  # Define the list of payment method choices
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
    ]

    # Retrieve a list of products from the database
    products = Product.objects.all()

    # Retrieve a list of warehouses from the database
    warehouses = Warehouse.objects.all()

    # Retrieve a list of taxes from the database
    taxes = Tax.objects.all()

    # Retrieve a list of discounts from the database
    discounts = Discount.objects.all()

    # Retrieve a list of suppliers from the database
    suppliers = Supplier.objects.all()

    # Iterate through each purchase and calculate payment status and due amount
    for expense in expenses:
        total_payment = Payment.objects.filter(expense=expense).aggregate(Sum('amount'))['amount__sum']

        if total_payment is None:
            total_payment = 0  # If no payments exist, set total_payment to 0

        # Determine the status based on the payment amount
        if total_payment == expense.amount:
            expense.payment_status = 'Paid'
        elif total_payment > 0:
            expense.payment_status = 'Partial'
        else:
            expense.payment_status = 'Unpaid'

        # Calculate the due amount
        expense.due_amount = expense.amount - total_payment

    # Render the HTML template with the list of purchases and products in the context
    return render(request, 'inventory_templates/expense_list.html', {
        'expense': expenses,
        'payment_methods': payment_methods,
        'payment': payment,
        'products': products,
        'warehouses': warehouses,
        'taxes': taxes,
        'discounts': discounts,
        'suppliers': suppliers})


    

@csrf_exempt
def make_payment_expense(request, expense_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('expense id from url: ', expense_id)
        try:
            expense = get_object_or_404(Expense, id=expense_id)
            print('expense inventory: ', expense)
        except Expense.DoesNotExist:
            return JsonResponse({'error': False, 'message': 'expense not found.'})

        # payment_date = request.POST.get('payment_date')
        # amount = request.POST.get('amount')
        # payment_method = request.POST.get('payment_method')
        # transaction_id = request.POST.get('transaction_id')
        print('payment_date: ', expense_id)
        payment_date = data['payment_date']
        amount = data['amount']
        payment_method = data['payment_method']
        transaction_id = data['transaction_id']
        print('payment_date: ', payment_date)

        payment = Payment(
            expense=expense,
            payment_date=payment_date,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id
        )

        payment.save()

        return JsonResponse({'success': True, 'message': 'Payment successfully recorded.'})
    else:
        return JsonResponse({'error': False, 'message': 'This endpoint only supports POST requests for payment processing.'})
    
def get_payment_data_expense(request, expense_id):
    if request.method == 'GET':
        # Retrieve the purchase and related payment
        expense = get_object_or_404(Expense, id=expense_id)
        # payment = Payment.objects.filter(purchase=purchase).first()
        try:
            payment = Payment.objects.filter(expense=expense).first()
            payment_data = {
                'payment_date': str(payment.payment_date),
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'transaction_id': payment.transaction_id,
            }
        except:
            payment_data = {
                'payment_date': '',
                'amount': '',
                'payment_method': '',
                'transaction_id': ''
            }

        print('expense id: ', expense)

        print('expense: ', expense)


        print('payment_date: ', payment_data['payment_date'])
        print('amount: ', payment_data['amount'])
        print('payment_method: ', payment_data['payment_method'])
        print('transaction_id: ', payment_data['transaction_id'])

        return JsonResponse({'success': True, 'payment_data': payment_data})
    else:
        return JsonResponse({'error': False, 'message': 'This endpoint only supports GET requests for viewing payments.'})
def delete_expense(request,expense_id):
   
    if request.method == 'POST':
        try:
            expense = Expense.objects.get(pk=expense_id)
            expense.delete()
            return JsonResponse({'success': True})
        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Brand not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
def add_payment_expense(request):
    if request.method == 'POST':
        # Get the data from the POST request
        payment_date = request.POST.get('payment_date')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        cheque_number = request.POST.get('cheque_number')
        card_number = request.POST.get('card_number')
        cash=request.POST.get('cash')
        voucher_no = request.POST.get('voucher_no')  # Assuming you have a voucher_number field in your form

        # Create a new Payment object without associating it with any expense or purchase
        payment = Payment(
            payment_date=payment_date,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=status,
            cheque_number=cheque_number,
            cash=cash,
            card_number=card_number,
        )

        # Save the new Payment object
        payment.save()

        # Try to associate the payment with an existing expense based on voucher number
        try:
            expense = Expense.objects.get(voucher_no=voucher_no)
            payment.expense = expense

            # Set additional payment-related fields in the Expense model if needed
            expense.payment_date = payment_date
            expense.amount_paid = amount
            expense.save()

            # Save the payment again to update the association
            payment.save()

            # Redirect to the payment expense list page or another appropriate page
            return redirect('expense_list')  # Adjust the URL name accordingly

        except Expense.DoesNotExist:
            # Handle the case where the expense with the provided voucher number does not exist
            messages.error(request, 'Expense not found for the provided voucher number.')

    return render(request, 'inventory_templates/add_payment_expense.html')

def dashboard(request):
    # Calculate Total Expense Amount
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_purchases = Purchase.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    # Calculate Stock Total
    total_stock = WarehouseProduct.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    # Calculate Warehouse Total
    total_warehouse = Warehouse.objects.count()
    # Calculate Purchase Returns Amount
    total_purchase_returns = PurchaseReturn.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'inventory_templates/home_content_inventory.html', {
        'total_expense': total_expense,
        'total_stock': total_stock,
        'total_warehouse': total_warehouse,
        'total_purchase_returns': total_purchase_returns,
        'total_purchases':total_purchases,
    })
def dashboard_data_view(request):
    # Calculate total expense
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    # Calculate total purchases
    total_purchases = Purchase.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    # Return data as JSON
    data = {
        'total_expense': total_expense,
        'total_purchases': total_purchases,
    }
    return JsonResponse(data)
def stock_data(request):
    # Calculate the start date (8 years ago from the current date)
    start_date = datetime.now() - timedelta(days=8 * 365)
    # Get the stock data for the last 8 years
    stock_data = WarehouseProduct.objects.filter(product__purchase__purchase_date__gte=start_date).values('product__purchase__purchase_date').annotate(closing_stock=Sum('quantity')).order_by('product__purchase__purchase_date')
    # Calculate opening and closing stock for each year
    opening_stock = []
    closing_stock = []
    prev_entry = None
    for entry in stock_data:
        if prev_entry is not None:
            opening_stock.append(prev_entry['closing_stock'])
        else:
            opening_stock.append(0)
        closing_stock.append(entry['closing_stock'])
        prev_entry = entry
    # Fill in missing years with zero opening and closing stock
    current_year = datetime.now().year
    for year in range(current_year - 8, current_year):
        if year not in [entry['product__purchase__purchase_date'].year for entry in stock_data]:
            opening_stock.append(0)
            closing_stock.append(0)
    # Prepare data for rendering in the template
    years = [entry['product__purchase__purchase_date'].year for entry in stock_data] + list(range(current_year - 8, current_year))
    # Return data as JSON
    data = {
        'years': years,
        'opening_stock': opening_stock,
        'closing_stock': closing_stock,
    }
    return JsonResponse(data)
def top_suppliers(request, month=None):
    # Get the current month if no month parameter is provided
    if month is None:
        month = datetime.now().month
    # Get the top 5 suppliers with the highest total amount spent in the specified month
    top_suppliers = Purchase.objects.filter(purchase_date__month=month).values('supplier__name').annotate(total_amount=Sum('grand_total')).order_by('-total_amount')[:5]
    # Create a list of dictionaries to represent the data
    top_suppliers_data = [{'name': supplier['supplier__name'], 'total_amount': float(supplier['total_amount'])} for supplier in top_suppliers]
    # Return data as JSON response
    data = {
        'top_suppliers': top_suppliers_data,
        'selected_month': month,
    }
    return JsonResponse(data)
def top_billers(request, month=None):
    # Get the current month if no month parameter is provided
    if month is None:
        month = datetime.now().month
    # Get the top 5 billers with the highest total amount spent in the specified month
    top_billers = Purchase.objects.filter(purchase_date__month=month).values('supplier__name').annotate(total_amount=Sum('grand_total')).order_by('-total_amount')[:5]
    # Create a list of dictionaries to represent the data
    top_billers_data = [{'name': biller['supplier__name'], 'total_amount': float(biller['total_amount'])} for biller in top_billers]
    # Return data as JSON response
    data = {
        'top_billers': top_billers_data,
        'selected_month': month,
    }
    return JsonResponse(data)
def combined_table_inventory(request):
    purchases = Purchase.objects.all()
    payments = Payment.objects.all()
    purchase_returns = PurchaseReturn.objects.all()
    invoices = PurchaseInvoice.objects.all()
    def get_status_badge(status):
        if status == '1':
            return format_html('<span class="badge badge-success">{}</span>', 'Paid')
        elif status == '2':
            return format_html('<span class="badge badge-warning">{}</span>', 'Pending')
        elif status == '3':
            return format_html('<span class="badge badge-danger">{}</span>', 'Unpaid')
        else:
            return format_html('<span class="badge badge-secondary">{}</span>', status)
    purchases_data = [
        {
            'Date': purchase.purchase_date,
            'Reference': purchase.invoice_number,
            'Customer/Supplier': purchase.supplier.name,
            'Mode': 'Purchase',
            'Status': get_status_badge(purchase.status),
            'Grand Price': purchase.grand_total,
        }
        for purchase in purchases
    ]
    payments_data = [
        {
            'Date': payment.payment_date,
            'Reference': payment.transaction_id,
            'Customer/Supplier': payment.purchase.supplier.name if payment.purchase and payment.purchase.supplier else 'N/A',
            'Mode': 'Payment',
            'Status': get_status_badge(payment.status),
            'Grand Price': payment.amount,
        }
        for payment in payments
    ]
    purchase_returns_data = [
        {
            'Date': return_data.purchase_return_date,
            'Reference': return_data.reference,
            'Customer/Supplier': return_data.supplier.name,
            'Mode': 'Purchase Return',
            'Status': get_status_badge(return_data.action),
            'Grand Price': return_data.amount,
        }
        for return_data in purchase_returns
    ]
    invoices_data = [
        {
            'Date': invoice.invoice_date,
            'Reference': invoice.invoice_number,
            'Customer/Supplier': invoice.supplier.name,
            'Mode': 'Invoice',
            'Status': get_status_badge(invoice.status),
            'Grand Price': invoice.shipping,
        }
        for invoice in invoices
    ]
    data = {
        'purchases': purchases_data,
        'payments': payments_data,
        'purchase_returns': purchase_returns_data,
        'invoices': invoices_data,
    }
    return JsonResponse(data, safe=False)

