
from django.shortcuts import get_object_or_404
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

from django.http import HttpResponseBadRequest
from datetime import date
from bus.models import CustomUser, TicketBooking, Coach, Route, PropularRoutes, Counter, District, Category, FAQ, TermsAndConditions, Profile, Bus, Seat, Booking, JourneyDateHistory, CancelTicket, BusStop, RoutePart, Tax, Payment, Company,Customers
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
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from accounts.models import Bank,BalanceTransfer,FinancialTransaction,PaymentInvoice,CreditVoucher,Bill,DebitVoucher,Notification,JournalEntry,LedgerGroup,LedgerEntry,Account
from inventory.models import Supplier,Biller,Expense,Purchase,Warehouse,Payment
from bus.models import Booking,Staffs,Counter
from django.http import JsonResponse, HttpResponseNotFound
from inventory.models import Payment as InventoryPayment
from bus.models import Payment as BusPayment
from accounts.models import PaymentInvoice as AccountsPayment
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db import transaction
from django.db.models import Sum, F, Value as V
from django.db.models import ExpressionWrapper, DecimalField
from django.db.models.functions import ExtractMonth, ExtractYear
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, TruncMonth
from django.views.decorators.http import require_http_methods
import calendar
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
# Create your views here.
# def add_bank(request):
#     if request.method == 'POST':
#         # Retrieve the data from the request
#         bank_name = request.POST.get('bank_name')
#         branch = request.POST.get('branch')
#         account_name = request.POST.get('account_name')
#         account_holder = request.POST.get('account_holder')
#         account_no = request.POST.get('account_no')
#         phone_number = request.POST.get('phone_number')
#         initial_balance = request.POST.get('initial_balance')
#         internet_banking_url = request.POST.get('internet_banking_url')
#         status = request.POST.get('status')

#         # Create a new Bank instance and save it to the database
#         bank = Bank(
#             bank_name=bank_name,
#             branch=branch,
#             account_name=account_name,
#             account_holder=account_holder,
#             account_no=account_no,
#             phone_number=phone_number,
#             initial_balance=initial_balance,
#             internet_banking_url=internet_banking_url,
#             status=status
#         )
#         bank.save()

#         return redirect('bank_list')  # Redirect to a list view of banks after adding


#     return render(request, 'accounts_templates/add_bank.html')

def bank_list(request):
    banks = Bank.objects.all() 
    suppliers = Supplier.objects.all()
    counters = Counter.objects.all()
    billers = Biller.objects.all() # Retrieve all banks from the database
    context = {
        'banks': banks,
        'suppliers':suppliers,
        'counters':counters,
        'billers':billers,

    }
    return render(request, 'accounts_templates/bank_list.html', context)


# def assign_bank(request, bank_id):
#     try:
#         # Retrieve the Bank with the given ID
#         bank = Bank.objects.get(id=bank_id)
#     except Bank.DoesNotExist:
#         return HttpResponseNotFound('Bank not found')

#     # Retrieve the Supplier, Counter, and Biller models using appropriate filters
#     supplier_queryset = Supplier.objects.all()
#     counter_queryset = Counter.objects.all()
#     biller_queryset = Biller.objects.all()
#     selected_value = request.POST.get('selected_value')

#     try:
#         # Iterate through the Supplier models and assign the account_name
#         for supplier in supplier_queryset:
#             supplier.account_name = bank.account_name
#             supplier.save()

#         # Iterate through the Counter models and assign the account_name
#         for counter in counter_queryset:
#             counter.account_name = bank.account_name
#             counter.credit_balance = bank.initial_balance
#             counter.save()

#         # Iterate through the Biller models and assign the account_name
#         for biller in biller_queryset:
#             biller.account_name = bank.account_name
#             biller.save()

#         # Set the initial_balance of the Bank to the credit balance of the associated Counter
#         associated_counter = None
#         if bank.assigned_select_name:
#             associated_counter = Counter.objects.filter(name=bank.assigned_select_name).first()
#             if associated_counter:
#                 bank.initial_balance = Decimal(associated_counter.credit_balance)

#         # Update the assigned_select_name
#         bank.assigned_select_name = selected_value
#         bank.save()

#         # Update the credit_balance of the associated Counter
#         if associated_counter:
#             associated_counter.credit_balance = bank.initial_balance
#             associated_counter.save()

#         # Print Bank information and associated Counter's credit balance
#         print(f'Bank data: {bank}')
#         if associated_counter:
#             print(f'Associated Counter credit balance: {associated_counter.credit_balance}')

#         return JsonResponse({'success': True, 'message': 'Account names and initial balance assigned successfully.'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)})
def add_bank(request):
    if request.method == 'POST':
        # Retrieve the data from the request
        bank_name = request.POST.get('bank_name')
        branch = request.POST.get('branch')
        account_name = request.POST.get('account_name')
        account_holder = request.POST.get('account_holder')
        account_no = request.POST.get('account_no')
        phone_number = request.POST.get('phone_number')
        initial_balance = request.POST.get('initial_balance')
        internet_banking_url = request.POST.get('internet_banking_url')
        status = request.POST.get('status')
        bank_availability = Bank.objects.filter(bank_name__iexact=bank_name, account_no=account_no).first()
        if not bank_availability:
            # Create a new Bank instance and save it to the database
            bank = Bank(
                bank_name=bank_name,
                branch=branch,
                account_name=account_name,
                account_holder=account_holder,
                account_no=account_no,
                phone_number=phone_number,
                initial_balance=initial_balance,
                internet_banking_url=internet_banking_url,
                status=status
            )
            bank.save()
            messages.success(request, "Bank added successfully")
            return redirect('bank_list')  # Redirect to a list view of banks after adding
        else:
            messages.error(request, "Bank with the same name already exists")
            return redirect('add_bank')
    return render(request, 'accounts_templates/add_bank.html')
def assign_bank(request, bank_id):
    try:
        # Retrieve the Bank with the given ID
        bank = Bank.objects.get(id=bank_id)
    except Bank.DoesNotExist:
        return HttpResponseNotFound('Bank not found')
    # Retrieve the Supplier, Counter, and Biller models using appropriate filters
    # supplier_queryset = Supplier.objects.all()
    # counter_queryset = Counter.objects.all()
    # biller_queryset = Biller.objects.all()
    selected_value = request.POST.get('selected_value')
    print('selected value: ', selected_value)
    selected_value_parts = selected_value.split('-')
    print('selected value parts: ', selected_value_parts)
    try:
        if len(selected_value_parts) == 2:
            prefix, id_number = selected_value_parts
            
            bank_name = bank.bank_name
            account_name = bank.account_name
            bank_account_no = bank.account_no

            counter_availabilty = Counter.objects.filter(bank_name=bank_name, account_name=account_name, bank_account_no=bank_account_no).first()
            supplier_availabilty = Supplier.objects.filter(bank_name=bank_name, account_name=account_name, bank_account_no=bank_account_no).first()
            biller_availabilty = Biller.objects.filter(bank_name=bank_name, account_name=account_name, bank_account_no=bank_account_no).first()
            if prefix == 'counter':
                try:
                    counter = Counter.objects.get(id=id_number)
                    if not counter_availabilty and not supplier_availabilty and not biller_availabilty:
                        counter.account_name = bank.account_name
                        counter.bank_name = bank.bank_name
                        counter.bank_account_no = bank.account_no
                        counter.credit_balance = bank.remaining_balance
                        counter.save()
                        return JsonResponse({'success': True, 'message': 'Account names and initial balance assigned successfully.'})
                    else:
                        return JsonResponse({'success': False, 'message':'Cannot assign Bank account. Bank account is already assigned'})
                except:
                    return JsonResponse({'success': False, 'message': 'Counter not found'})
            if prefix == 'supplier':
                try:
                    supplier = Supplier.objects.get(id=id_number)
                    if not counter_availabilty and not supplier_availabilty and not biller_availabilty:
                        supplier.account_name = account_name
                        supplier.bank_name = bank_name
                        supplier.bank_account_no = bank_account_no
                        supplier.save()
                        return JsonResponse({{'success': f"Bank account succesfully assigned to {supplier.name}"}})
                    else:
                        return JsonResponse({'error': 'Cannot assign Bank account. Bank account is already assigned'})
                except:
                    return JsonResponse({'error': 'Counter not found'})
            if prefix == 'supplier':
                try:
                    biller = Biller.objects.get(id=id_number)
                    if not counter_availabilty and not supplier_availabilty and not biller_availabilty:
                        biller.account_name = account_name
                        biller.bank_name = bank_name
                        biller.bank_account_no = bank_account_no
                        biller.save()
                        return JsonResponse({{'success': f"Bank account succesfully assigned to {biller.name}"}})
                    else:
                        return JsonResponse({'error': 'Cannot assign Bank account. Bank account is already assigned'})
                except:
                    return JsonResponse({'error': 'Counter not found'})

        associated_counter = None
        if bank.assigned_select_name:
            associated_counter = Counter.objects.filter(name=bank.assigned_select_name).first()
            if associated_counter:
                bank.initial_balance = Decimal(associated_counter.credit_balance)
        # Update the assigned_select_name
        bank.assigned_select_name = selected_value
        bank.save()
        # Update the credit_balance of the associated Counter
        if associated_counter:
            associated_counter.credit_balance = bank.initial_balance
            associated_counter.save()
        # Print Bank information and associated Counter's credit balance
        print(f'Bank data: {bank}')
        if associated_counter:
            print(f'Associated Counter credit balance: {associated_counter.credit_balance}')
        return JsonResponse({'success': True, 'message': 'Account names and initial balance assigned successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



def edit_bank(request, bank_id):
    if request.method == 'POST':
        data = request.POST  # Assuming you are sending data via a POST request

        try:
            bank = get_object_or_404(Bank, id=bank_id)
        except Bank.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bank not found.'})

        # Update payment details based on the data received
        bank.bank_name = data.get('bank_name', bank.bank_name)
        bank.branch = data.get('branch', bank.branch)
        bank.account_name = data.get(
            'account_name', bank.account_name)
        bank.account_holder = data.get(
            'account_holder', bank.account_holder)
        bank.account_no = data.get(
            'account_no', bank.account_no)
        bank.phone_number = data.get(
            'phone_number', bank.phone_number)
        bank.initial_balance = data.get(
            'initial_balance', bank.initial_balance)
        bank.internet_banking_url = data.get(
            'internet_banking_url', bank.internet_banking_url)
        bank.status = data.get(
            'status', bank.status)
        

        # Save the updated payment
        bank.save()

        return JsonResponse({'success': True, 'message': 'Data  updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'This endpoint only supports POST requests for editing payments.'})
    


def delete_bank(request, bank_id):

    try:
        # Get the Purchase object or return a 404 response if not found
        bank = get_object_or_404(Bank, id=bank_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the purchase
            bank.delete()
            return JsonResponse({'success': True, 'message': 'bank deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except Bank.DoesNotExist:
        # If the purchase doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'Bank not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})
    




def create_balance_transfer(request):
    if request.method == 'POST':
        # Process the submitted data
        from_account_id = request.POST.get('from_account')
        to_account_id = request.POST.get('to_account')
        initial_balance = Decimal(request.POST.get('initial_balance'))
        note = request.POST.get('note')

        # Retrieve the bank instances based on the selected account IDs
        from_account = Bank.objects.get(id=from_account_id)
        to_account = Bank.objects.get(id=to_account_id)

        # Create a new BalanceTransfer object and save it to the database
        balance_transfer = BalanceTransfer(
            from_account=from_account,
            to_account=to_account,
            initial_balance=initial_balance,
            note=note
        )
        balance_transfer.save()

        # Update the remaining balance of the 'from_account'
        from_account.remaining_balance -= initial_balance
        from_account.save()

        # Update the remaining balance of the 'to_account'
        to_account.remaining_balance += initial_balance
        to_account.save()

        messages.success(request, 'Balance transfer created successfully.')
        return redirect('transfer_list')  # Redirect to the list view of balance transfers

    # Get a list of bank accounts for the dropdowns
    bank_accounts = Bank.objects.all()

    return render(request, 'accounts_templates/create_balance_transfer.html', {'bank_accounts': bank_accounts})

def transfer_list(request):
    transfers = BalanceTransfer.objects.all()  # Retrieve all balance transfers from the database

    # Retrieve the account numbers for all banks
    banks = Bank.objects.all()  # Retrieve all banks from the database
    account_numbers = {}

    for bank in banks:
        account_numbers[bank.id] = bank.account_no

    context = {
        'transfers': transfers,
        'account_numbers': account_numbers,  # Pass the account numbers to the context
    }
    return render(request, 'accounts_templates/transfer_list.html', context)


def edit_transfer(request, transfer_id):
    if request.method == 'POST':
        data = request.POST  # Assuming you are sending data via a POST request

        try:
            transfer = get_object_or_404(BalanceTransfer, id=transfer_id)
        except BalanceTransfer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Balance Transfer not found.'})

        # Update transfer details based on the data received
        from_account_id = data.get('from_account')
        to_account_id = data.get('to_account')
        initial_balance = data.get('initial_balance')
        note = data.get('note')

        # Validate that the selected accounts exist
        from_account = get_object_or_404(Bank, id=from_account_id)
        to_account = get_object_or_404(Bank, id=to_account_id)

        # Update the transfer details
        transfer.from_account = from_account
        transfer.to_account = to_account
        transfer.initial_balance = initial_balance
        transfer.note = note

        # Save the updated transfer
        transfer.save()

        return JsonResponse({'success': True, 'message': 'Balance Transfer updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'This endpoint only supports POST requests for editing transfers.'})
    



def delete_transfer(request, transfer_id):

    try:
        # Get the Purchase object or return a 404 response if not found
        transfer= get_object_or_404(BalanceTransfer, id=transfer_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the purchase
            transfer.delete()
            return JsonResponse({'success': True, 'message': 'Payment deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except transfer.DoesNotExist:
        # If the purchase doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'Payment not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})
def add_transaction(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        
        transaction = FinancialTransaction()
        transaction.status = request.POST.get('status')
        transaction.voucher_number = request.POST.get('voucher_number')
        transaction.account_id = request.POST.get('account_id')
        transaction.payment_type = request.POST.get('payment_type')
        transaction.amount = request.POST.get('amount')
        transaction.date = request.POST.get('date')
        transaction.reference = request.POST.get('reference')
        transaction.payment_receipt = request.FILES.get('payment_receipt')
        transaction.payment_note = request.POST.get('payment_note')

        group_object = None

        if category == 'supplier':
            group_id = request.POST.get('supplier_id')
            group_object = get_object_or_404(Supplier, pk=group_id)
        elif category == 'biller':
            group_id = request.POST.get('biller_id')
            group_object = get_object_or_404(Biller, pk=group_id)
        elif category == 'purchases':
            group_id = request.POST.get('purchases_id')
            group_object = get_object_or_404(Purchase, pk=group_id)
        elif category == 'expense':
            group_id = request.POST.get('expense_id')
            group_object = get_object_or_404(Expense, pk=group_id)
        elif category == 'counter':  # Assuming 'counter' is a valid category
            group_id = request.POST.get('counter_id')
            group_object = get_object_or_404(Counter, pk=group_id)

        transaction.group = group_object
        transaction.save()

        # Redirect to a success page or the transaction detail page
        return redirect('financial_transaction_list')  # Replace 'success_page' with your URL name

    banks = Bank.objects.all()
    suppliers = Supplier.objects.all()
    billers = Biller.objects.all()
    expenses = Expense.objects.all()
    purchases = Purchase.objects.all()
    counters = Counter.objects.all()  # Retrieve all counters

    return render(request, 'accounts_templates/add_transaction.html', {
        'banks': banks,
        'suppliers': suppliers,
        'billers': billers,
        'expenses': expenses,
        'purchases': purchases,
        'counters': counters,  # Include 'counters' in the context
    })

def add_payment_invoice(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        
        payment_invoice = PaymentInvoice()
        payment_invoice.status = request.POST.get('status')
        payment_invoice.invoice_number = request.POST.get('invoice_number')
        payment_invoice.account_id = request.POST.get('account_id')
        payment_invoice.payment_type = request.POST.get('payment_type')
        payment_invoice.amount = request.POST.get('amount')
        payment_invoice.date = request.POST.get('date')
        payment_invoice.reference = request.POST.get('reference')
        payment_invoice.payment_receipt = request.FILES.get('payment_receipt')
        payment_invoice.payment_note = request.POST.get('payment_note')

        group_object = None

        if category == 'supplier':
            group_id = request.POST.get('supplier_id')
            group_object = get_object_or_404(Supplier, pk=group_id)
        elif category == 'biller':
            group_id = request.POST.get('biller_id')
            group_object = get_object_or_404(Biller, pk=group_id)
        elif category == 'purchases':
            group_id = request.POST.get('purchases_id')
            group_object = get_object_or_404(Purchase, pk=group_id)
        elif category == 'expense':
            group_id = request.POST.get('expense_id')
            group_object = get_object_or_404(Expense, pk=group_id)

        payment_invoice.group = group_object
        payment_invoice.save()

        messages.success(request, 'Payment Invoice added successfully.')
        return redirect('payment_invoice_list')  # Redirect to the invoice detail page or other page

    banks = Bank.objects.all()
    suppliers = Supplier.objects.all()
    billers = Biller.objects.all()
    expenses = Expense.objects.all()
    purchases = Purchase.objects.all()

    return render(request, 'accounts_templates/add_payment_invoice.html', {
        'banks': banks,
        'suppliers': suppliers,
        'billers': billers,
        'expenses': expenses,
        'purchases': purchases,
    })
def get_transaction_details(request, transaction_id):
    try:
        # Retrieve FinancialTransaction based on the provided transaction_id
        financial_transaction = get_object_or_404(FinancialTransaction, id=transaction_id)

        # Retrieve related payment details if available
        payment_details = None
        payment = Payment.objects.filter(transaction_id=financial_transaction.reference).first()

        if payment:
            payment_details = {
                'payment_date': str(payment.payment_date),
                'amount': str(payment.amount),
                'payment_method': payment.payment_method,
                'cheque_number': payment.cheque_number,
                'card_number': payment.card_number,
                'status': payment.status,
            }

           
            if payment.purchase:
                purchase_details = {
                    'purchase_id': payment.purchase.id,
                    'purchase_product': str(payment.purchase.product),
                    'purchase_date': str(payment.purchase.purchase_date),
                    'purchase_supplier': str(payment.purchase.supplier),
                    'purchase_warehouse': str(payment.purchase.warehouse),
                    'purchase_invoice_number': payment.purchase.invoice_number,
                    'order_tax': payment.purchase.order_tax,
                    'order_discount': payment.purchase.order_discount,
                    'grand_total': payment.purchase.grand_total,
                    'created_by_name': payment.purchase.created_by.get_full_name() if payment.purchase.created_by else 'N/A',
                    'created_by_email': payment.purchase.created_by.email if payment.purchase.created_by else 'N/A',
                    'created_by_phone_number': payment.purchase.created_by.phone_number if payment.purchase.created_by else 'N/A',
                    'created_by_address': payment.purchase.created_by.address if payment.purchase.created_by else 'N/A',
                    'purchase_supplier_name': payment.purchase.supplier.name,
                    'purchase_supplier_email': payment.purchase.supplier.email,
                    'purchase_supplier_phone': payment.purchase.supplier.phone,
                }
                
                payment_details['purchase_details'] = purchase_details

        response_data = {
            'transaction_id': financial_transaction.reference,
            'payment_date': str(financial_transaction.date),
            'amount': str(financial_transaction.amount),
            'payment_method': financial_transaction.payment_type,
            'transaction_status': financial_transaction.status,
            'voucher_number': financial_transaction.voucher_number,
            'account': financial_transaction.account.account_name,
            'payment_type': financial_transaction.payment_type,
            'financial_transaction_amount': str(financial_transaction.amount),
            'financial_transaction_date': str(financial_transaction.date),
            'reference': financial_transaction.reference,
            'payment_receipt': financial_transaction.payment_receipt.url if financial_transaction.payment_receipt else None,
            'payment_note': financial_transaction.payment_note,
            'payment_details': payment_details,
        }

        return JsonResponse(response_data)

    except FinancialTransaction.DoesNotExist:
        return JsonResponse({'error': f'Financial Transaction with ID {transaction_id} not found'}, status=404)
    except Payment.DoesNotExist:
        return JsonResponse({'error': f'Payment with ID {transaction_id} not found'}, status=404)
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
def financial_transaction_list(request):
    transactions = FinancialTransaction.objects.all()
    bank_accounts = Bank.objects.all() 
    
    return render(request, 'accounts_templates/financial_transaction_list.html', {
        'transactions': transactions,
        'bank_accounts': bank_accounts,
    })

def payment_invoice_list(request):
    invoices = PaymentInvoice.objects.all()
    bank_accounts = Bank.objects.all() 
    return render(request, 'accounts_templates/payment_invoice_list.html', {'invoices': invoices,'bank_accounts': bank_accounts,})

def get_expense_details(request, invoice_id):
    invoice = get_object_or_404(PaymentInvoice, pk=invoice_id)


    try:
        expense = Expense.objects.get(voucher_no=invoice.invoice_number)
    except Expense.DoesNotExist:

        return JsonResponse({"error": "Expense not found for this invoice."}, status=404)

  
    try:
        warehouse = Warehouse.objects.get(id=expense.warehouse_id)
    except Warehouse.DoesNotExist:
   
        return JsonResponse({"error": "Warehouse not found for this expense."}, status=404)


    try:
        payment = Payment.objects.get(expense=expense)
    except Payment.DoesNotExist:
        payment = None  

    sub_category = expense.sub_category
    if sub_category:
        category = sub_category.category
    else:
        sub_category = None
        category = None


    expense_data = {
        "id": expense.id,
        "date": expense.date,
        "warehouse_name": expense.warehouse.name,
        "expense_type": expense.expense_type,
        "amount": expense.amount,
        "purchase_note": expense.purchase_note,
        "warehouse_location": warehouse.location,
        "warehouse_phone_number": warehouse.phone_number,
        "warehouse_email": warehouse.email,
        "warehouse_address_country": warehouse.address_country,
        "warehouse_address_city": warehouse.address_city,
        "warehouse_address_postal_code": warehouse.address_postal_code,
        "payment_data": {
            "payment_date": payment.payment_date if payment else None,
            "payment_amount": payment.amount if payment else None,
            "payment_method": payment.payment_method if payment else None,
            "transaction_id": payment.transaction_id if payment else None,
            "payment_status": payment.status if payment else None,
        },
        "voucher_number": invoice.invoice_number,
        "sub_category": sub_category.name if sub_category else None,
        "category": category.name if category else None,
    }

    return JsonResponse(expense_data)

@require_POST
def edit_transaction(request, transaction_id):
    try:
        # Get the transaction object based on the transaction_id
        transaction = FinancialTransaction.objects.get(pk=transaction_id)

        # Ensure the user is authorized to edit this transaction if needed

        # Extract data from the request
        status = request.POST.get('status')
        voucher_number = request.POST.get('voucher_number')
        account_id = request.POST.get('account')
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        reference = request.POST.get('reference')

        # Update the transaction object
        transaction.status = status
        transaction.voucher_number = voucher_number
        transaction.account_id = account_id
        transaction.payment_type = payment_type
        transaction.amount = amount
        transaction.date = date
        transaction.reference = reference

        # Save the changes to the transaction
        transaction.save()

        response_data = {'success': True, 'message': 'Transaction updated successfully.'}
    except FinancialTransaction.DoesNotExist:
        response_data = {'success': False, 'message': 'Transaction does not exist.'}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}

    return JsonResponse(response_data)


def delete_transaction(request, transaction_id):

    try:
        # Get the Purchase object or return a 404 response if not found
        transaction = get_object_or_404(FinancialTransaction, id=transaction_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the purchase
            transaction.delete()
            return JsonResponse({'success': True, 'message': 'transaction deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except Bank.DoesNotExist:
        # If the purchase doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'transaction not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})
    









@require_POST
def edit_payment_invoice(request, invoice_id):
    try:
        # Get the payment invoice object based on the invoice_id
        payment_invoice = PaymentInvoice.objects.get(pk=invoice_id)

        # Ensure the user is authorized to edit this payment invoice if needed

        # Extract data from the request
        status = request.POST.get('status')
        invoice_number = request.POST.get('invoice_number')
        account_id = request.POST.get('account')
        payment_type = request.POST.get('payment_type')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        reference = request.POST.get('reference')

        # Update the payment invoice object
        payment_invoice.status = status
        payment_invoice.invoice_number = invoice_number
        payment_invoice.account_id = account_id
        payment_invoice.payment_type = payment_type
        payment_invoice.amount = amount
        payment_invoice.date = date
        payment_invoice.reference = reference

        # Save the changes to the payment invoice
        payment_invoice.save()

        response_data = {'success': True, 'message': 'Payment invoice updated successfully.'}
    except PaymentInvoice.DoesNotExist:
        response_data = {'success': False, 'message': 'Payment invoice does not exist.'}
    except Exception as e:
        response_data = {'success': False, 'message': str(e)}

    return JsonResponse(response_data)

def delete_invoice(request, invoice_id):
    try:
        # Get the PaymentInvoice object or return a 404 response if not found
        payment_invoice = get_object_or_404(PaymentInvoice, id=invoice_id)

        # Check if the request is a POST request (for safety)
        if request.method == 'POST':
            # Delete the payment invoice
            payment_invoice.delete()
            return JsonResponse({'success': True, 'message': 'Payment invoice deleted successfully'})
        else:
            # Return a "Method Not Allowed" response for non-POST requests
            return JsonResponse({'success': False, 'message': 'Method not allowed for this URL'})
    except PaymentInvoice.DoesNotExist:
        # If the payment invoice doesn't exist, return a "Not Found" response
        return JsonResponse({'success': False, 'message': 'Payment invoice not found'})
    except Exception as e:
        # Handle other exceptions, e.g., database errors
        return JsonResponse({'success': False, 'message': str(e)})
    


def create_credit_voucher(request):
    if request.method == 'POST':
        # Get the data from the request
        date = request.POST.get('date')
        payment_gateway = request.POST.get('payment_gateway')
        payment_mode = request.POST.get('payment_mode')
        cheque_number = request.POST.get('cheque_number')
        reference = request.POST.get('reference')
        amount = request.POST.get('amount')
        particular = request.POST.get('particular')

        # Retrieve the bank and generate the voucher number
        bank_id = request.POST.get('account')  # Retrieve selected bank from the form
        bank = Bank.objects.get(id=bank_id)

        # Create a CreditVoucher instance and set the bank and other fields
        credit_voucher = CreditVoucher(
            date=date,
            payment_gateway=payment_gateway,
            payment_mode=payment_mode,
            cheque_number=cheque_number,
            reference=reference,
            bank=bank,
            amount=amount,
            particular=particular,
            account=bank.account_name  # Set the 'account' field to the selected bank's account name
        )

        # Save the CreditVoucher instance, which will generate the voucher number
        credit_voucher.save()

        return redirect('credit_voucher_list')  # Replace 'credit_voucher_list' with your URL name for listing credit vouchers

    # Get a list of bank accounts and other data
    bank_accounts = Bank.objects.all()
    types = FinancialTransaction.PAYMENT_TYPE_CHOICES

    return render(request, 'accounts_templates/credit_voucher_create.html', {'bank_accounts': bank_accounts, 'types': types})



def create_debit_voucher(request):
    if request.method == 'POST':
 
        date = request.POST.get('date')
        payment_gateway = request.POST.get('payment_gateway')
        payment_mode = request.POST.get('payment_mode')
        cheque_number = request.POST.get('cheque_number')
        reference = request.POST.get('reference')
        amount = request.POST.get('amount')
        particular = request.POST.get('particular')

       
        bank_id = request.POST.get('account') 
        bank = Bank.objects.get(id=bank_id)

     
        debit_voucher = DebitVoucher(
            date=date,
            payment_gateway=payment_gateway,
            payment_mode=payment_mode,
            cheque_number=cheque_number,
            reference=reference,
            bank=bank,
            amount=amount,
            particular=particular,
            account=bank.account_name 
        )

        debit_voucher.save()

        return redirect('debit_voucher_list')  


    bank_accounts = Bank.objects.all()
    types = FinancialTransaction.PAYMENT_TYPE_CHOICES

    return render(request, 'accounts_templates/debit_voucher_create.html', {'bank_accounts': bank_accounts, 'types': types})


def debit_voucher_list(request):
    debit_vouchers = DebitVoucher.objects.all()  # Retrieve all credit vouchers
    return render(request, 'accounts_templates/debit_voucher_list.html', {'debit_vouchers': debit_vouchers})

def get_debit_voucher_details(request, voucher_id):
    debit_voucher = get_object_or_404(DebitVoucher, pk=voucher_id)

    try:
  
        payment = Payment.objects.get(cheque_number=debit_voucher.cheque_number)
        payment_details = {
            'payment_date': payment.payment_date,
            'payment_method': payment.payment_method,
            'transaction_id': payment.transaction_id,
            'status': payment.status,
            'amount': payment.amount,
            'expense_id': payment.expense.id if payment.expense else None,
            'purchase_id': payment.purchase.id if payment.purchase else None,
        }
        if payment.purchase:
                purchase_details = {
                    'purchase_id': payment.purchase.id,
                    'purchase_product': str(payment.purchase.product),
                    'purchase_date': str(payment.purchase.purchase_date),
                    'purchase_supplier': str(payment.purchase.supplier),
                    'purchase_warehouse': str(payment.purchase.warehouse),

                    'purchase_warehouse_email':str(payment.purchase.warehouse.email),
                    'purchase_warehouse_phone':str(payment.purchase.warehouse.phone),
                     'warehouse_address': f"{payment.purchase.warehouse.address_country}, {payment.purchase.warehouse.address_city}, {payment.purchase.warehouse.address_postal_code}",


                    'purchase_invoice_number': payment.purchase.invoice_number,
                    'order_tax': payment.purchase.order_tax,
                    'order_discount': payment.purchase.order_discount,
                    'grand_total': payment.purchase.grand_total,
                    'created_by_name': payment.purchase.created_by.get_full_name() if payment.purchase.created_by else 'N/A',
                    'created_by_email': payment.purchase.created_by.email if payment.purchase.created_by else 'N/A',
                    'created_by_phone_number': payment.purchase.created_by.phone_number if payment.purchase.created_by else 'N/A',
                    'created_by_address': payment.purchase.created_by.address if payment.purchase.created_by else 'N/A',
                    'purchase_supplier_name': payment.purchase.supplier.name,
                    'purchase_supplier_email': payment.purchase.supplier.email,
                    'purchase_supplier_phone': payment.purchase.supplier.phone,
                }
                
                payment_details['purchase_details'] = purchase_details
    except Payment.DoesNotExist:

        payment_details = None

    data = {
        'date': debit_voucher.date,
        'payment_gateway': debit_voucher.payment_gateway,
        'payment_mode': debit_voucher.payment_mode,
        'cheque_number': debit_voucher.cheque_number,
        'reference': debit_voucher.reference,
        'amount': debit_voucher.amount,
        'particular': debit_voucher.particular,
        'account_name': debit_voucher.account,  
        'voucher_number': debit_voucher.voucher_number,
        'payment_details': payment_details 
    }

    return JsonResponse(data)

def get_credit_voucher_details(request, voucher_id):
    credit_voucher = get_object_or_404(CreditVoucher, pk=voucher_id)

    try:
  
        payment = Payment.objects.get(cheque_number=credit_voucher.cheque_number)
        payment_details = {
            'payment_date': payment.payment_date,
            'payment_method': payment.payment_method,
            'transaction_id': payment.transaction_id,
            'status': payment.status,
            'amount': payment.amount,
            'expense_id': payment.expense.id if payment.expense else None,
            'purchase_id': payment.purchase.id if payment.purchase else None,
        }
        if payment.purchase:
                purchase_details = {
                    'purchase_id': payment.purchase.id,
                    'purchase_product': str(payment.purchase.product),
                    'purchase_date': str(payment.purchase.purchase_date),
                    'purchase_supplier': str(payment.purchase.supplier),
                    'purchase_warehouse': str(payment.purchase.warehouse),

                    'purchase_warehouse_email':str(payment.purchase.warehouse.email),
                    'purchase_warehouse_phone':str(payment.purchase.warehouse.phone),
                     'warehouse_address': f"{payment.purchase.warehouse.address_country}, {payment.purchase.warehouse.address_city}, {payment.purchase.warehouse.address_postal_code}",


                    'purchase_invoice_number': payment.purchase.invoice_number,
                    'order_tax': payment.purchase.order_tax,
                    'order_discount': payment.purchase.order_discount,
                    'grand_total': payment.purchase.grand_total,
                    'created_by_name': payment.purchase.created_by.get_full_name() if payment.purchase.created_by else 'N/A',
                    'created_by_email': payment.purchase.created_by.email if payment.purchase.created_by else 'N/A',
                    'created_by_phone_number': payment.purchase.created_by.phone_number if payment.purchase.created_by else 'N/A',
                    'created_by_address': payment.purchase.created_by.address if payment.purchase.created_by else 'N/A',
                    'purchase_supplier_name': payment.purchase.supplier.name,
                    'purchase_supplier_email': payment.purchase.supplier.email,
                    'purchase_supplier_phone': payment.purchase.supplier.phone,
                }
                
                payment_details['purchase_details'] = purchase_details
    except Payment.DoesNotExist:

        payment_details = None

    data = {
        'date': credit_voucher.date,
        'payment_gateway': credit_voucher.payment_gateway,
        'payment_mode': credit_voucher.payment_mode,
        'cheque_number': credit_voucher.cheque_number,
        'reference': credit_voucher.reference,
        'amount': credit_voucher.amount,
        'particular': credit_voucher.particular,
        'account_name': credit_voucher.account,  
        'voucher_number': credit_voucher.voucher_number,
        'payment_details': payment_details 
    }

    return JsonResponse(data)


def credit_voucher_list(request):
    credit_vouchers = CreditVoucher.objects.all()  # Retrieve all credit vouchers
    return render(request, 'accounts_templates/credit_voucher_list.html', {'credit_vouchers': credit_vouchers})

def create_bill(request):
    if request.method == 'POST':
        # Retrieve staff and date range from the form
        staff_id = request.POST.get('staff_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Get the staff object
        staff = Staffs.objects.get(id=staff_id)

        # Query the bills for the selected staff within the date range
        bills = Bill.objects.filter(staff=staff, bill_date__range=[start_date, end_date])

        # Calculate total ticket details
        total_tickets = 0
        cancellation_details = []

        for bill in bills:
            cancellation_details.extend(bill.approved_cancellations())

        total_tickets = len(cancellation_details)

        context = {
            'staff': staff,
            'start_date': start_date,
            'end_date': end_date,
            'total_tickets': total_tickets,
            'cancellation_details': cancellation_details
        }

        return render(request, 'your_template.html', context)
    else:
        staffs = Staffs.objects.all()
        print('staffs:',staffs)
    return render(request, 'accounts_templates/create_bill.html', {'staffs': staffs})

def total_transactions(request):
    # Calculate the total payment transactions across all three models
    inventory_total = InventoryPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    bus_total = BusPayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    accounts_total = AccountsPayment.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate the total card, cash, and bank paymen0t amounts for each model
    inventory_card_total = InventoryPayment.objects.filter(payment_method='Card').aggregate(Sum('amount'))['amount__sum'] or 0
    inventory_cash_total = InventoryPayment.objects.filter(payment_method='Cash').aggregate(Sum('amount'))['amount__sum'] or 0
    inventory_bank_total = InventoryPayment.objects.filter(payment_method='Bank').aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate the total card, cash, and bank payments for the Bus model
    bus_card_total = BusPayment.objects.filter(payment_type=1).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    bus_cash_total = BusPayment.objects.filter(payment_type=2).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    bus_bank_total = BusPayment.objects.filter(payment_type=3).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    accounts_card_total = AccountsPayment.objects.filter(payment_type='Card').aggregate(Sum('amount'))['amount__sum'] or 0
    accounts_cash_total = AccountsPayment.objects.filter(payment_type='Cash').aggregate(Sum('amount'))['amount__sum'] or 0
    accounts_bank_total = AccountsPayment.objects.filter(payment_type='Bank').aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate the total card, cash, and bank payments across all models
    total_card = inventory_card_total + bus_card_total + accounts_card_total
    total_cash = inventory_cash_total + bus_cash_total + accounts_cash_total
    total_bank = inventory_bank_total + bus_bank_total + accounts_bank_total

    # Calculate the total payment transactions across all models
    total_payment_transactions = inventory_total + bus_total + accounts_total
    inventory_model=InventoryPayment.objects.all()
    BusPayment_model=BusPayment.objects.all()
    accounts_model=AccountsPayment.objects.all()
    all_payments = list(inventory_model) + list(BusPayment_model) + list(accounts_model)

    return render(request, 'accounts_templates/transection.html', {
        'total_payment_transactions': total_payment_transactions,
        'total_card': total_card,
        'total_cash': total_cash,
        'total_bank': total_bank,
        'inventory_model':inventory_model,
        'BusPayment_model':BusPayment_model,
        'accounts_model': accounts_model,
        'all_payments': all_payments
    })



def expense(request):
    total_bus_payment = BusPayment.objects.all()
    total_bill = Bill.objects.all()
    total_expense_model = Expense.objects.all()

    # Calculate total expenses for the entire period
    total_bus_payment_amount = total_bus_payment.aggregate(Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')
    total_bill_amount = total_bill.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = total_expense_model.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Calculate monthly booking amounts
    monthly_booking_amounts = Booking.objects.annotate(
        month=ExtractMonth('booking_date')
    ).values('month').annotate(
        total_booking_amount=Sum('price')
    ).order_by('month')

    # Create a dictionary to store the total booking amounts for each month
    monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly amounts
    for monthly_amount in monthly_booking_amounts:
        month = monthly_amount['month']
        monthly_amounts[month] = monthly_amount['total_booking_amount']

    return render(request, 'accounts_templates/total_expense.html', {
        'total_bus_payment': total_bus_payment,
        'total_bus_payment_amount': total_bus_payment_amount,
        'total_bill': total_bill,
        'total_bill_amount': total_bill_amount,
        'total_expense': total_expense,
        'january_amount': monthly_amounts[1],
        'february_amount': monthly_amounts[2],
        'march_amount': monthly_amounts[3],
        'april_amount': monthly_amounts[4],
        'may_amount': monthly_amounts[5],
        'june_amount': monthly_amounts[6],
        'july_amount': monthly_amounts[7],
        'august_amount': monthly_amounts[8],
        'september_amount': monthly_amounts[9],
        'october_amount': monthly_amounts[10],
        'november_amount': monthly_amounts[11],
        'december_amount': monthly_amounts[12],
    })


def revenue_view(request):
    # Calculate the total income from PaymentInvoices with a status of 'completed'
    completed_invoices = PaymentInvoice.objects.filter(status='completed')
    
    # Calculate monthly income from PaymentInvoices
    monthly_invoice_income = completed_invoices.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    # Create a dictionary to store the total invoice income for each month
    invoice_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly invoice amounts
    for monthly_income in monthly_invoice_income:
        month = monthly_income['month']
        invoice_monthly_amounts[month] = monthly_income['total_invoice_income']

    # Calculate the total invoice income
    invoice_total = sum(invoice_monthly_amounts.values())

    # Calculate the total income from Payments
    payments = BusPayment.objects.all()
    
    # Calculate monthly income from Payments
    monthly_payment_income = payments.annotate(
        month=ExtractMonth('date_paid')  # Use the correct date field, which is 'date_paid'
    ).values('month').annotate(
        total_payment_income=Sum('amount_paid')
    ).order_by('month')

    # Create a dictionary to store the total payment income for each month
    payment_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly payment amounts
    for monthly_income in monthly_payment_income:
        month = monthly_income['month']
        payment_monthly_amounts[month] = monthly_income['total_payment_income']

    # Calculate the total income and revenue
    total_income = sum(invoice_monthly_amounts.values()) + sum(payment_monthly_amounts.values())
    total_revenue = sum(payment_monthly_amounts.values())

    # Calculate total income per month
    total_monthly_income = {month: invoice_monthly_amounts[month] + payment_monthly_amounts[month] for month in range(1, 13)}

    return render(request, 'accounts_templates/revenue_template.html', {
        'total_income': total_income,
        'total_revenue': total_revenue,
        'invoice_total': invoice_total,
        'invoice_monthly_amounts': invoice_monthly_amounts,
        'payment_monthly_amounts': payment_monthly_amounts,
        'total_monthly_income': total_monthly_income,
    })

def income_vs_expense(request):
    # Calculate the total income from PaymentInvoices with a status of 'completed'
    completed_invoices = PaymentInvoice.objects.filter(status='completed')

    # Calculate monthly income from PaymentInvoices
    monthly_invoice_income = completed_invoices.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    # Create dictionaries to store the total monthly income for payments and invoices
    invoice_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly invoice amounts
    for monthly_income in monthly_invoice_income:
        month = monthly_income['month']
        invoice_monthly_amounts[month] = monthly_income['total_invoice_income']

    # Calculate the total invoice income
    invoice_total = sum(invoice_monthly_amounts.values())

    # Calculate the total income from Payments
    payments = BusPayment.objects.all()

    # Calculate monthly income from Payments
    monthly_payment_income = payments.annotate(
        month=ExtractMonth('date_paid')
    ).values('month').annotate(
        total_payment_income=Sum('amount_paid')
    ).order_by('month')

    # Create a dictionary to store the total payment income for each month
    payment_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly payment amounts
    for monthly_income in monthly_payment_income:
        month = monthly_income['month']
        payment_monthly_amounts[month] = monthly_income['total_payment_income']

    # Calculate the total income and revenue
    total_income = sum(invoice_monthly_amounts.values()) + sum(payment_monthly_amounts.values())
    total_revenue = sum(payment_monthly_amounts.values())

    # Calculate total expense per month from the Expense model
    expenses = Expense.objects.all()
    monthly_expense = expenses.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_expense=Sum('amount')
    ).order_by('month')

    # Calculate the total expense from the Bill model
    bills = Bill.objects.all()
    monthly_expense = monthly_expense.annotate(
        bill_expense=Sum(F('amount') + V(0), output_field=DecimalField(max_digits=10, decimal_places=2))
    )

    # Create dictionaries to store the total monthly expenses for payments and bills
    monthly_expense_payments = {month: Decimal('0.00') for month in range(1, 13)}
    monthly_expense_bill = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionaries with the calculated monthly expense amounts for payments
    for monthly_exp in monthly_expense:
        month = monthly_exp['month']
        monthly_expense_payments[month] = monthly_exp['total_expense']

    # Calculate the total expense from the Bill model
    monthly_bill_expense = bills.annotate(
        month=ExtractMonth('bill_date')
    ).values('month').annotate(
        total_bill_expense=Sum('amount')
    ).order_by('month')

    # Populate the dictionary with the calculated monthly bill expenses
    for monthly_bill in monthly_bill_expense:
        month = monthly_bill['month']
        monthly_expense_bill[month] = monthly_bill['total_bill_expense']

    # Calculate the total profit
    total_profit = total_income - (sum(monthly_expense_payments.values()) + sum(monthly_expense_bill.values()))

   

    # Calculate the total income per month
    total_income_per_month = [payment_monthly_amounts.get(month, Decimal('0.00')) + invoice_monthly_amounts.get(month, Decimal('0.00')) for month in range(1, 13)]

    # Calculate the total expenses per month
    total_expense_per_month = [monthly_expense_payments.get(month, Decimal('0.00')) + monthly_expense_bill.get(month, Decimal('0.00')) for month in range(1, 13)]

    # Calculate the monthly profit per month
    monthly_profit = [total_income - total_expense for total_income, total_expense in zip(total_income_per_month, total_expense_per_month)]

    return render(request, 'accounts_templates/income_vs_expense_template.html', {
        'total_income': total_income,
        'total_revenue': total_revenue,
        'invoice_total': invoice_total,
        'total_expense': sum(monthly_expense_payments.values()) + sum(monthly_expense_bill.values()),
        'total_profit': total_profit,
        'invoice_monthly_amounts': invoice_monthly_amounts,
        'payment_monthly_amounts': payment_monthly_amounts,
        'monthly_expense_payments': monthly_expense_payments,
        'monthly_expense_bill': monthly_expense_bill,
        'total_income_per_month': total_income_per_month,
        'total_expense_per_month': total_expense_per_month,
        'monthly_profit': monthly_profit,
    })


def profit_loss(request):
    # Calculate the total income from PaymentInvoices with a status of 'completed'
    completed_invoices = PaymentInvoice.objects.filter(status='completed')

    # Calculate monthly income from PaymentInvoices
    monthly_invoice_income = completed_invoices.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    # Create a dictionary to store the total invoice income for each month
    invoice_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly invoice amounts
    for monthly_income in monthly_invoice_income:
        month = monthly_income['month']
        invoice_monthly_amounts[month] = monthly_income['total_invoice_income']

    # Calculate the total invoice income
    invoice_total = sum(invoice_monthly_amounts.values())

    # Calculate the total income from Payments
    payments = BusPayment.objects.all()

    # Calculate monthly income from Payments
    monthly_payment_income = payments.annotate(
        month=ExtractMonth('date_paid')
    ).values('month').annotate(
        total_payment_income=Sum('amount_paid')
    ).order_by('month')

    # Create a dictionary to store the total payment income for each month
    payment_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly payment amounts
    for monthly_income in monthly_payment_income:
        month = monthly_income['month']
        payment_monthly_amounts[month] = monthly_income['total_payment_income']

    # Calculate the total income and revenue
    total_income = sum(invoice_monthly_amounts.values()) + sum(payment_monthly_amounts.values())
    total_revenue = sum(payment_monthly_amounts.values())

    # Calculate total expense per month from the Expense model
    expenses = Expense.objects.all()
    monthly_expense = expenses.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_expense=Sum('amount')
    ).order_by('month')

    # Calculate the total expense from the Bill model
    bills = Bill.objects.all()
    monthly_expense = monthly_expense.annotate(
        bill_expense=Sum(F('amount') + V(0), output_field=DecimalField(max_digits=10, decimal_places=2)
    ))

    # Create dictionaries to store the total monthly expenses for payments and bills
    monthly_expense_payments = {month: Decimal('0.00') for month in range(1, 13)}
    monthly_expense_bill = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionaries with the calculated monthly expense amounts for payments
    for monthly_exp in monthly_expense:
        month = monthly_exp['month']
        monthly_expense_payments[month] = monthly_exp['total_expense']

    # Calculate the total expense from the Bill model
    bills = Bill.objects.all()
    monthly_bill_expense = bills.annotate(
        month=ExtractMonth('bill_date')
    ).values('month').annotate(
        total_bill_expense=Sum('amount')
    ).order_by('month')

    # Populate the dictionary with the calculated monthly bill expenses
    for monthly_bill in monthly_bill_expense:
        month = monthly_bill['month']
        monthly_expense_bill[month] = monthly_bill['total_bill_expense']

    total_profit = total_income - (sum(monthly_expense_payments.values()) + sum(monthly_expense_bill.values()))

   

    # Calculate the total income per month
    total_income_per_month = [payment_monthly_amounts.get(month, Decimal('0.00')) + invoice_monthly_amounts.get(month, Decimal('0.00')) for month in range(1, 13)]

    # Calculate the total expenses per month
    total_expense_per_month = [monthly_expense_payments.get(month, Decimal('0.00')) + monthly_expense_bill.get(month, Decimal('0.00')) for month in range(1, 13)]

    # Calculate the monthly profit per month
    monthly_profit = [total_income - total_expense for total_income, total_expense in zip(total_income_per_month, total_expense_per_month)]

    # Calculate the total loss (if expenses exceed income)
    total_loss = max(0, (sum(monthly_expense_payments.values()) + sum(monthly_expense_bill.values()) - total_income))
    monthly_loss = [max(0, total_expense - total_income) for total_income, total_expense in zip(total_income_per_month, total_expense_per_month)]

    # Create dictionaries for monthly profit and monthly loss
   

    return render(request, 'accounts_templates/profit_loss_template.html', {
        'total_income': total_income,
        'total_revenue': total_revenue,
        'invoice_total': invoice_total,
        'total_expense': sum(monthly_expense_payments.values()) + sum(monthly_expense_bill.values()),
        'total_profit': total_profit,
        'total_loss': total_loss,
        'invoice_monthly_amounts': invoice_monthly_amounts,
        'payment_monthly_amounts': payment_monthly_amounts,
        'monthly_expense_payments': monthly_expense_payments,
        'monthly_expense_bill': monthly_expense_bill,
        'monthly_profit': monthly_profit,
        'monthly_loss': monthly_loss,
    })


def trail_balance(request):
    credit_transactions = None
    debit_transactions = None
    total_debit = 0.0
    total_credit = 0.0

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        credit_transactions = CreditVoucher.objects.filter(date__range=[from_date, to_date])
        debit_transactions = DebitVoucher.objects.filter(date__range=[from_date, to_date])

        # Calculate total debit amount
        total_debit = debit_transactions.aggregate(total_debit=Sum('amount'))['total_debit'] or 0.0

        # Calculate total credit amount
        total_credit = credit_transactions.aggregate(total_credit=Sum('amount'))['total_credit'] or 0.0

    return render(request, 'accounts_templates/trail_balance.html', {
        'credit_transactions': credit_transactions,
        'debit_transactions': debit_transactions,
        'total_debit': total_debit,
        'total_credit': total_credit,
    })



def dashboard(request):
    # Calculate total transactions amount
    total_bus_payment = BusPayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')
    total_bill = Bill.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_invoice = PaymentInvoice.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    total_transactions = total_bus_payment + total_bill + total_expense + total_invoice

    # Calculate total expenses
    total_expenses = total_expense

    # Calculate total income
    total_income = total_invoice

    # Calculate total net income
    total_net_income = total_income - total_expenses

    # Calculate monthly income from PaymentInvoices
    monthly_invoice_income = PaymentInvoice.objects.filter(status='completed').annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    # Create a dictionary to store the total invoice income for each month
    invoice_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly invoice amounts
    for monthly_income in monthly_invoice_income:
        month = monthly_income['month']
        invoice_monthly_amounts[month] = monthly_income['total_invoice_income']

    # Calculate monthly expenses
    monthly_expense = Expense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_expense=Sum('amount')
    ).order_by('month')

    # Create a dictionary to store the total monthly expenses
    monthly_expense_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    # Populate the dictionary with the calculated monthly expense amounts
    for monthly_exp in monthly_expense:
        month = monthly_exp['month']
        monthly_expense_amounts[month] = monthly_exp['total_expense']

    total_counter = Counter.objects.count()


    return render(request, 'accounts_templates/home_content_accounts.html', {
        'total_transactions': total_transactions,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'total_net_income': total_net_income,
        'invoice_monthly_amounts': invoice_monthly_amounts,
        'monthly_expense_amounts': monthly_expense_amounts,
        'total_counter':total_counter
    })


def get_monthly_income_data():
    completed_invoices = PaymentInvoice.objects.filter(status='completed')
    monthly_invoice_income = completed_invoices.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    invoice_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    for monthly_income in monthly_invoice_income:
        month = monthly_income['month']
        invoice_monthly_amounts[month] = monthly_income['total_invoice_income']

    payments = BusPayment.objects.all()
    monthly_payment_income = payments.annotate(
        month=ExtractMonth('date_paid')
    ).values('month').annotate(
        total_payment_income=Sum('amount_paid')
    ).order_by('month')

    payment_monthly_amounts = {month: Decimal('0.00') for month in range(1, 13)}

    for monthly_income in monthly_payment_income:
        month = monthly_income['month']
        payment_monthly_amounts[month] = monthly_income['total_payment_income']

    return {
        'invoice_monthly_amounts': invoice_monthly_amounts,
        'payment_monthly_amounts': payment_monthly_amounts,
    }

def get_monthly_expense_data():
    expenses = Expense.objects.all()
    monthly_expense = expenses.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_expense=Sum('amount')
    ).order_by('month')

    bills = Bill.objects.all()
    monthly_expense = monthly_expense.annotate(
        bill_expense=Sum(F('amount') + V(0), output_field=DecimalField(max_digits=10, decimal_places=2))
    )

    monthly_expense_payments = {month: Decimal('0.00') for month in range(1, 13)}
    monthly_expense_bill = {month: Decimal('0.00') for month in range(1, 13)}

    for monthly_exp in monthly_expense:
        month = monthly_exp['month']
        monthly_expense_payments[month] = monthly_exp['total_expense']

    monthly_bill_expense = bills.annotate(
        month=ExtractMonth('bill_date')
    ).values('month').annotate(
        total_bill_expense=Sum('amount')
    ).order_by('month')

    for monthly_bill in monthly_bill_expense:
        month = monthly_bill['month']
        monthly_expense_bill[month] = monthly_bill['total_bill_expense']

    return {
        'monthly_expense_payments': monthly_expense_payments,
        'monthly_expense_bill': monthly_expense_bill,
    }

def cash_flow_chart_data(request):
    monthly_income_data = get_monthly_income_data()
    monthly_expense_data = get_monthly_expense_data()

    cash_flow_data = {
        'labels': list(monthly_income_data['invoice_monthly_amounts'].keys()),
        'datasets': [
            {
                'label': 'Income',
                'data': list(monthly_income_data['invoice_monthly_amounts'].values()),
                'backgroundColor': '#5DADE2',
            },
            {
                'label': 'Expense',
                'data': [
                    monthly_expense_data['monthly_expense_payments'][month] + monthly_expense_data['monthly_expense_bill'][month]
                    for month in range(1, 13)
                ],
                'backgroundColor': '#FF5733',
            },
        ],
    }

    return JsonResponse(cash_flow_data)




@require_http_methods(["GET"])
def recent_vouchers(request):
    # Get the most recent credit and debit vouchers
    recent_credit_vouchers = CreditVoucher.objects.all().order_by('-date')[:5]
    recent_debit_vouchers = DebitVoucher.objects.all().order_by('-date')[:5]

    # Format the data for JSON response
    combined_vouchers_data = [
        {
            'Type': 'Credit',
            'Date': voucher.date.strftime('%Y-%m-%d'),
            'Account': voucher.account,
            'Voucher No': voucher.voucher_number,
            'Payment Type': voucher.payment_mode,
            'Amount': str(voucher.amount),
        }
        for voucher in recent_credit_vouchers
    ] + [
        {
            'Type': 'Debit',
            'Date': voucher.date.strftime('%Y-%m-%d'),
            'Account': voucher.account,
            'Voucher No': voucher.voucher_number,
            'Payment Type': voucher.payment_mode,
            'Amount': str(voucher.amount),
        }
        for voucher in recent_debit_vouchers
    ]

    # Sort combined data by date
    combined_vouchers_data.sort(key=lambda x: x['Date'], reverse=True)

    return JsonResponse(combined_vouchers_data, safe=False)


def counter_credit_balance(request):
    # Fetch all counters with their credit balances
    counters = Counter.objects.all()


    counter_data = []

    # Iterate through each counter and retrieve name and credit balance
    for counter in counters:
        counter_info = {
            'name': counter.name,
            'credit_balance': str(counter.credit_balance),
        }
        print('counter_info:',counter_info)
        counter_data.append(counter_info)

    return JsonResponse(counter_data, safe=False)



@require_http_methods(["GET"])
def recent_bookings(request):
    # Get the most recent bookings along with the customer name and amount paid
    recent_bookings = Booking.objects.filter(is_paid=True).order_by('-booking_date')[:5]

    # Format the data for JSON response
    bookings_data = [
        {
            'Customer Name': booking.customer.name if booking.customer else 'N/A',
            'Amount Paid': str(booking.payment_set.aggregate(Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')),
        }
        for booking in recent_bookings
    ]

    return JsonResponse(bookings_data, safe=False)


def income_vs_expense_json(request):
    # Calculate monthly income from PaymentInvoices
    invoice_monthly_amounts = PaymentInvoice.objects.filter(status='completed').annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_invoice_income=Sum('amount')
    ).order_by('month')

    # Calculate monthly income from BusPayments
    payment_monthly_amounts = BusPayment.objects.annotate(
        month=ExtractMonth('date_paid')
    ).values('month').annotate(
        total_payment_income=Sum('amount_paid')
    ).order_by('month')

    # Calculate total income and revenue
    total_income = sum(invoice_monthly_amounts.values_list('total_invoice_income', flat=True)) + sum(payment_monthly_amounts.values_list('total_payment_income', flat=True))
    total_revenue = sum(payment_monthly_amounts.values_list('total_payment_income', flat=True))

    # Calculate monthly expenses from Expense model
    monthly_expense_payments = Expense.objects.annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(
        total_expense=Sum('amount')
    ).order_by('month')

    # Calculate monthly expenses from Bill model
    monthly_expense_bill = Bill.objects.annotate(
        month=ExtractMonth('bill_date')
    ).values('month').annotate(
        total_bill_expense=Sum('amount')
    ).order_by('month')

    # Prepare the data for JSON response
    data = {
        'total_income': total_income,
        'total_revenue': total_revenue,
        'invoice_total': sum(invoice_monthly_amounts.values_list('total_invoice_income', flat=True)),
        'total_expense': sum(monthly_expense_payments.values_list('total_expense', flat=True)) + sum(monthly_expense_bill.values_list('total_bill_expense', flat=True)),
        'total_profit': total_income - (sum(monthly_expense_payments.values_list('total_expense', flat=True)) + sum(monthly_expense_bill.values_list('total_bill_expense', flat=True))),
        'monthly_data': [],
    }

    # Add monthly breakdown to the data
    for month in range(1, 13):
        monthly_data = {
            'month': month,
            'total_income': invoice_monthly_amounts.filter(month=month).values_list('total_invoice_income', flat=True).first() or Decimal('0.00'),
            'total_expense': monthly_expense_payments.filter(month=month).values_list('total_expense', flat=True).first() or Decimal('0.00'),
            'monthly_profit': data['total_income'] - data['total_expense'],
        }
        data['monthly_data'].append(monthly_data)

    return JsonResponse(data)




def active_user_list(request):
    User = get_user_model()

    # Filter active users based on the last_active field
    active_users = User.objects.filter(last_active__gte=timezone.now() - timezone.timedelta(minutes=5)).values('user_id', 'username', 'phone_number', 'last_active')

    return JsonResponse(list(active_users), safe=False)


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'accounts_templates/supplier_list.html', {'suppliers': suppliers})


def biller_list(request):
    billers = Biller.objects.all()
    return render(request, 'accounts_templates/biller_list.html', {'billers': billers})


def customer_list(request):
    user = request.user
    company = user.company
    company = Company.objects.get(id=company.id)

    all_customers = Customers.objects.filter(company=company)

    context = {
        'all_customers': all_customers,
    }
    return render(request, 'accounts_templates/customer_list.html', context)

from django.views.decorators.http import require_GET
@login_required
@require_GET
def notification_list(request):
    # Fetch all notifications for the logged-in user, both read and unread
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')

    # Mark only unread notifications as read
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    # Convert notifications to a list of dictionaries for JSON serialization
    notifications_data = [
        {
            'message': notification.message,
            'timestamp': notification.timestamp.isoformat(),  # Convert to ISO format for JSON compatibility
            'is_read': notification.is_read,
        }
        for notification in notifications
    ]

    # Return a JSON response
    return JsonResponse({'notifications': notifications_data})

@login_required
def create_journal_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        particular = request.POST.get('particular')

        # Retrieve the bank and generate the voucher number
        bank_id = request.POST.get('account')
        bank = Bank.objects.get(id=bank_id)

        # Retrieve debit and credit amounts from the form
        debit_amount = request.POST.get('debit_amount')
        credit_amount = request.POST.get('credit_amount')

        # Create JournalEntry for debit
        JournalEntry.objects.create(
            date=date,
            particular=particular,
            account=bank,
            amount=debit_amount,
            entry_type='dr',  # Assuming 'dr' represents a debit entry
            user=request.user
        )

        # Create JournalEntry for credit
        JournalEntry.objects.create(
            date=date,
            particular=particular,
            account=bank,
            amount=credit_amount,
            entry_type='cr',  # Assuming 'cr' represents a credit entry
            user=request.user
        )

        return JsonResponse({'success': True})

    # If the request is not POST, retrieve all banks for the form
    banks = Account.objects.all()

    return render(request, 'accounts_templates/create_journal.html', {'accounts': banks})


def save_journal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data['date']
        particular = data['particular']
        debit_accounts = data['debit_accounts']
        credit_accounts = data['credit_accounts']
        both_accounts = data['both_accounts']
        no_account = data['no_account']
        print('data: ', data)

        print('date: ', date)
        print('particular: ', particular)
        print('debit_accounts: ', debit_accounts)
        print('credit_accounts: ', credit_accounts)
        
        # this is structure of the date--> data: {'debit_accounts': [['13', 10], ['13', 20]], 'credit_accounts': [['16', 30]], 'csrfmiddlewaretoken': 'QqjKoPrYK6nRpx1TyyubHM4IvvpM8GCBYQ1nfMhSvPXSuUgUdKBSn6Aq3gB8Gr2N', 'date': '2023-12-14', 'particular': ''}
        # In `'debit_accounts': [['13', 10], ['13', 20]]` --> '13' is the id of the Account number and 10 and 20 are the corresponding amount
        if not both_accounts and not no_account:
            if date and particular and debit_accounts and credit_accounts:
                for debit_account in debit_accounts:
                    if len(debit_account)  < 3:
                        account_id =int(debit_account[0])
                        amount = debit_account[1]
                        try:
                            account = Account.objects.get(id=account_id)
                        except Account.DoesNotExist:
                            account = None
                            return JsonResponse({'error': 'Account does not exist'})
                        
                        if account is not None and len(debit_account) == 2:
                            JournalEntry.objects.create(
                                date=date,
                                particular=particular,
                                account=account,
                                amount=amount,
                                entry_type='dr',
                                user=request.user
                            )

                        else:
                            return JsonResponse({'error': 'Account does not exist or You didn\'t enter the debit amount'})

                    else:
                        return JsonResponse({'error': 'An account can\'t be Debit and Credit at the same time.'})
                    
                for credit_account in credit_accounts:
                    if len(debit_account)  < 3:
                        account_id =int(credit_account[0])
                        amount = credit_account[1]
                        try:
                            account = Account.objects.get(id=account_id)
                        except Account.DoesNotExist:
                            account = None
                            return JsonResponse({'error': 'Account does not exist'})
                        
                        if account is not None and len(debit_account) == 2:
                            JournalEntry.objects.create(
                                date=date,
                                particular=particular,
                                account=account,
                                amount=amount,
                                entry_type='cr',
                                user=request.user
                            )

                        else:
                            return JsonResponse({'error': 'Account does not exist or You didn\'t enter the debit amount'})

                    else:
                        return JsonResponse({'error': 'An account can\'t be Debit and Credit at the same time.'})
                    
            else:
                return JsonResponse({'error': 'Missing Data'})
            
        else:
            return JsonResponse({'error': 'Fields cannot be empty or an account can\'t be Debit and Credit at the same time'})

        return JsonResponse({'success': 'Journal Entries saved Succesfully'})


def journal_list(request):
    # Retrieve start and end date parameters from the request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Set default values for start and end dates
    start_date = datetime.min.date()
    end_date = datetime.max.date()

    # Parse start date if provided
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    # Parse end date if provided
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Filter journal entries based on date range
    journal_entries = JournalEntry.objects.filter(date__range=(start_date, end_date))

    return render(request, 'accounts_templates/journal_list.html', {'journal_entries': journal_entries})




def create_ledger(request):
    ledger_groups = LedgerGroup.objects.all()
    
    context = {
        'ledger_groups': ledger_groups
    }
    print('context: ', context)
    return render(request, 'accounts_templates/create_ledger.html', context)


def ledger_view(request):
    ledger_groups = LedgerGroup.objects.all()
    
    context = {
        'ledger_groups': ledger_groups
    }
    print('context: ', context)
    
    return render(request, 'accounts_templates/ledger_view.html', context)


def get_accounts_name(request):
    if request.method == 'GET':
        ledger_group_id = request.GET.get('group_name', '')
        print('ledger_group: ', ledger_group_id)
        if ledger_group_id :
            try:
                ledger_group = LedgerGroup.objects.get(id=ledger_group_id)
            except LedgerGroup.DoesNotExist:
                ledger_group = None
                return JsonResponse({'error': 'Ledger Group could not be found'})
            
            if ledger_group is not None:
                group_name = ledger_group.name
                print('group name test: ', group_name)

                biller_group, created_at = LedgerGroup.objects.get_or_create(name='Biller')

                supplier_group, created_at = LedgerGroup.objects.get_or_create(name='Supplier')

                accs = Account.objects.all()
                for acc in accs:
                    print('accs: ', acc.account_id)
                if group_name == 'Supplier' or group_name == 'supplier':
                    suppliers = Supplier.objects.all()
                    for supplier in suppliers:
                        # not a good idea to send the queryset in the JsonResponse, so serialize the data
                        try:
                            account = Account.objects.get(account_id=supplier.supplier_id)
                        except Account.DoesNotExist:
                            account = None
                        
                        if account is None:
                            supplier_account = Account.objects.create(account_id=supplier.supplier_id, name=supplier.name)
                            supplier_account.group = supplier_group

                            supplier_account.save()

                    accounts = Account.objects.filter(group=supplier_group)
                    suppliers_data = serialize('json', accounts, fields=('id', 'name'))
                    print('suppliers_data: ', suppliers_data)
                    return JsonResponse({'data': suppliers_data})
                
                elif group_name == 'Biller' or group_name == 'biller':
                    billers = Biller.objects.all()
                    for biller in billers:
                        print('billers: ', biller)
                        # not a good idea to send the queryset in the JsonResponse, so serialize the data
                        try:
                            account = Account.objects.get(account_id=biller.biller_id)
                            print('biller accounts: ', account.name)
                        except Account.DoesNotExist:
                            account = None
                        
                        if account is None:
                            print('account is None')
                            biller_account = Account.objects.create(account_id=biller.biller_id, name=biller.name)
                            biller_account.group = biller_group

                            biller_account.save()

                    accounts = Account.objects.filter(group=biller_group)
                    billers_data = serialize('json', accounts, fields=('id', 'name'))
                    print('billers_data: ', billers_data)
                    return JsonResponse({'data': billers_data})
                
                else:
                    try:
                        accounts = ledger_group.accounts.all()
                    except Account.DoesNotExist:
                        accounts = None

                    if accounts is not None:
                        general_data = serialize('json', accounts, fields=('id', 'name'))
                        print('general_data: ', general_data)
                        return JsonResponse({'data': general_data})
        
            else:
                return JsonResponse({'error': 'Ledger Group could not be found'})


def save_ledger(request):
    if request.method == 'POST':
        ledger_date = request.POST.get('ledger_date')
        group_id = request.POST.get('group_name')
        ledger_id = request.POST.get('ledger_name')
        ledger_type = request.POST.get('ledger_type')
        reference = request.POST.get('reference')
        transaction_type = request.POST.get('mode')
        amount = request.POST.get('ledger_amount')
        description = request.POST.get('details', '')


        print('ledger_date: ', ledger_date)
        print('group_name: ', group_id)
        print('ledger_id: ', ledger_id)
        print('ledger_type: ', ledger_type)
        print('reference: ', reference)
        print('mode: ', transaction_type)

        if ledger_date and group_id and ledger_id and ledger_type and reference and transaction_type and amount:
            try:
                account = Account.objects.get(id=ledger_id)
            except Account.DoesNotExist:
                account = None
            print('account: ', account)
            try:
                ledger_group = LedgerGroup.objects.get(id=group_id)
            except LedgerGroup.DoesNotExist:
                ledger_group = None
                return JsonResponse({'error': 'Error finding Group. Please check if the group exists'})

            if account is not None and ledger_group is not None:
                LedgerEntry.objects.create(
                    transaction_type=transaction_type,
                    amount=amount,
                    account=account,
                    description=description,
                    ledger_type=ledger_type,
                    date=ledger_date,
                    reference=reference,
                    group=ledger_group,
                )
            else:
                return JsonResponse({'error': 'Could not find the Account name'})
        
        else:
            return JsonResponse({'error': 'Please fill all the details'})

    return JsonResponse({'success': f'Ledger for {account.name} created Successfully'})

def ledger_list(request):
    return render(request, 'accounts_templates/ledger_list.html')