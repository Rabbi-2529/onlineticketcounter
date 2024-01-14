from django.db import models
from django.urls import reverse
from inventory.models import Supplier,Warehouse
from bus.models import Counter
from bus.models import Staffs,Booking
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Max
from django.utils import timezone
from bus.models import CustomUser

class Bank(models.Model):
    BANK_STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    bank_name = models.CharField(max_length=100, verbose_name='Bank Name')
    branch = models.CharField(max_length=100, verbose_name='Branch')
    account_name = models.CharField(max_length=100, verbose_name='Account Name')
    account_holder = models.CharField(max_length=100, verbose_name='Account Holder')
    account_no = models.CharField(max_length=20, verbose_name='Account No')
    phone_number = models.CharField(max_length=15, verbose_name='Phone')
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Initial Balance')
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Remaining Balance')
    internet_banking_url = models.URLField(verbose_name='Internet Banking URL')
    status = models.CharField(max_length=10, choices=BANK_STATUS_CHOICES, default='active', verbose_name='Status')
    # New field to store assigned name
    assigned_select_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Assigned  Name')
    def __str__(self):
        return self.bank_name
    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'
    def save(self, *args, **kwargs):
        # Set default value for remaining_balance same as initial_balance
        if not self.remaining_balance:
            self.remaining_balance = self.initial_balance
        super().save(*args, **kwargs)



class BalanceTransfer(models.Model):
    from_account = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='transfers_from')
    to_account = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='transfers_to')
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('balance_transfer_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Transfer from {self.from_account.bank_name} to {self.to_account.bank_name}"


class FinancialTransaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    )

    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default='pending', verbose_name='Status')
    voucher_number = models.CharField(max_length=20, verbose_name='Voucher Number')
    account = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Account')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name='Payment Type')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    date = models.DateField(verbose_name='Date')
    reference = models.CharField(max_length=100, verbose_name='Reference')
    payment_receipt = models.FileField(upload_to='payment_receipts/', blank=True, null=True, verbose_name='Payment Receipt')
    payment_note = models.TextField(blank=True, verbose_name='Payment Note')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    group = GenericForeignKey('content_type', 'object_id')
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Counter')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Supplier')
   

    def __str__(self):
        return f"{self.group} - {self.voucher_number}"

    class Meta:
        verbose_name = 'Financial Transaction'
        verbose_name_plural = 'Financial Transactions'


class PaymentInvoice(models.Model):
    INVOICE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('check', 'Check'),
    )

    status = models.CharField(max_length=10, choices=INVOICE_STATUS_CHOICES, default='pending', verbose_name='Status')
    invoice_number = models.CharField(max_length=20, verbose_name='Invoice Number')
    account = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Account')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name='Payment Type')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    date = models.DateField(verbose_name='Date')
    reference = models.CharField(max_length=100, verbose_name='Reference')
    payment_receipt = models.FileField(upload_to='payment_receipts/', blank=True, null=True, verbose_name='Payment Receipt')
    payment_note = models.TextField(blank=True, verbose_name='Payment Note')

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    group = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.group} - {self.invoice_number}"

    class Meta:
        verbose_name = 'Payment Invoice'
        verbose_name_plural = 'Payment Invoices'



class CreditVoucher(models.Model):
    date = models.DateField()
    payment_gateway = models.CharField(max_length=100)
    account=models.CharField(max_length=200)
    payment_mode = models.CharField(max_length=100)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=100)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='credit_vouchers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    particular = models.TextField()
    voucher_number = models.CharField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.voucher_number:
            # Generate a unique voucher number with a timestamp prefix
            timestamp_prefix = timezone.now().strftime('%Y%m%d%H%M%S')
            max_voucher = DebitVoucher.objects.aggregate(Max('voucher_number'))['voucher_number__max']
            if max_voucher is None:
                max_voucher = 0

            # Generate the next voucher number with the timestamp prefix
            self.voucher_number = f'igl-{timestamp_prefix}-{max_voucher + 1}'

        super(CreditVoucher, self).save(*args, **kwargs)
        


class DebitVoucher(models.Model):
    date = models.DateField()
    payment_gateway = models.CharField(max_length=100)
    account = models.CharField(max_length=100, null=True)
    payment_mode = models.CharField(max_length=100)
    cheque_number = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=100)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='debit_vouchers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    particular = models.TextField()
    voucher_number = models.CharField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.voucher_number:
            max_voucher = DebitVoucher.objects.aggregate(Max('voucher_number'))['voucher_number__max']

            if max_voucher is None:
                max_voucher = 0
            else:
                # Convert the string to an integer
                max_voucher = int(max_voucher.lstrip('igl-'))

            # Convert the integer part to a string before concatenating
            self.voucher_number = f'igl-{max_voucher + 1}'

        super(DebitVoucher, self).save(*args, **kwargs)

class Bill(models.Model):

    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    cancel_date = models.DateField()
    bill_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=50)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Bill for Order {self.order_number}"

    @staticmethod
    def get_staff_cancellation_details(staff, start_date, end_date):
        """
        Retrieve cancellation details for a specific staff within a date range.

        Args:
            staff (Staffs): The staff for whom to retrieve the details.
            start_date (date): The start date of the date range.
            end_date (date): The end date of the date range.

        Returns:
            QuerySet: A QuerySet of cancellation details.
        """
        return Bill.objects.filter(
            staff=staff,
            cancel_date__range=(start_date, end_date)
        )
    

class LedgerGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Group Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ledger Group'
        verbose_name_plural = 'Ledger Groups'


class Account(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(LedgerGroup, on_delete=models.SET_NULL, max_length=100, related_name='accounts', blank=True, null=True)
    account_id = models.CharField(max_length=8, unique=True, editable=False)
    # account_id = models.CharField(max_length=8, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.account_id:
            # if self.group.name == 'Supplier':
            #     last_account = Account.objects.order_by('-id').first()
            #     if last_account:
            #         last_id = int(last_account.account_id[3:])
            #         new_id = last_id + 1
            #     else:
            #         new_id = 1
            #     self.account_id = f'445{str(new_id).zfill(3)}'
            
            # elif self.group.name == 'Biller':
            #     last_account = Account.objects.order_by('-id').first()
            #     if last_account:
            #         last_id = int(last_account.account_id[3:])
            #         new_id = last_id + 1
            #     else:
            #         new_id = 1
            #     self.account_id = f'445{str(new_id).zfill(3)}'

            if not self.group or self.group.name == 'General':
                last_account = Account.objects.order_by('-id').first()
                if last_account:
                    last_id = int(last_account.account_id[3:])
                    new_id = last_id + 1
                else:
                    new_id = 1
                self.account_id = f'333{str(new_id).zfill(3)}'
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    ENTRY_TYPES = (
        ('dr', 'Debit'),
        ('cr', 'Credit'),
    )

    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    particular = models.TextField()
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_entry_type_display()}: {self.amount} for {self.particular}"


    class Meta:
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
class LedgerEntry(models.Model):
    TRANSACTION_TYPES = (
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, max_length=50, null=True, blank=True)
    ledger_type = models.CharField(max_length=50)
    date = models.DateField()
    reference = models.CharField(max_length=100)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(LedgerGroup, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.amount} for {self.description}"

    class Meta:
        verbose_name = 'Ledger Entry'
        verbose_name_plural = 'Ledger Entries'


class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message}"
    