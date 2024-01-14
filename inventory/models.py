from django.db import models
from bus.models import *
import random


# Create your models here.

class Tax(models.Model):
    name = models.CharField(max_length=100)
    # Define choices for tax rates
    TAX_RATE_CHOICES = (
        (7.5, '7.5%'),
        (10, '10%'),
        (15, '15%'),
        (20, '20%'),
        # Add more choices as needed
    )
    # For example, 7.5% tax rate
    rate = models.DecimalField(max_digits=5, decimal_places=2, choices=TAX_RATE_CHOICES,)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    # For example, $10 discount
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=250)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address_country = models.CharField(max_length=50, blank=True, null=True)
    address_city = models.CharField(max_length=50, blank=True, null=True)
    address_postal_code = models.CharField(
        max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CategoryItem(models.Model):
    CATEGORY_CHOICES = (
        ('1', 'Bus Seats'),
        ('2', 'Bus Mirrors'),
        ('3', 'Bus Windows'),
        ('4', 'Bus Tires'),
        ('5', 'Bus Lights'),
        ('6', 'Bus Engines'),
        ('7', 'Bus Electronics'),
        ('8', 'Bus Interior Accessories'),
        ('9', 'Bus Exterior Accessories'),
        ('10', 'Bus Audio Systems'),
        ('11', 'Bus Safety Equipment'),
        ('12', 'Bus GPS Systems'),
        ('13', 'Bus Cameras'),
        ('14', 'Bus Air Conditioning'),
        ('15', 'Bus Seating Covers'),
        ('16', 'Bus Wheels and Rims'),
        ('17', 'Bus Flooring'),
        ('18', 'Bus Maintenance Tools'),
        ('19', 'Bus Cleaning Supplies'),
        ('20', 'Bus Safety Signage'),
        ('21', 'Bus Parts and Accessories'),
        # Add more category choices as needed
    )

    name = models.CharField(
        max_length=250, primary_key=True, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class SubCategory(models.Model):

    category = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand_images/', null=True, blank=True)

    def __str__(self):
        return self.name
class ExpenseCategory(models.Model):
    EXPENSE_CATEGORY_CHOICES = [
        ('1', 'Fuel'),
        ('2', 'Maintenance'),
        ('3', 'Insurance'),
        ('4', 'Repairs'),
        ('5', 'Other'),
        ('6', 'Transportation'),
        ('7', 'Miscellaneous'),
        ('8', 'Electronics'),
        ('9', 'Electrics'),
        ('10', 'Hospital/Medical'),
        ('11', 'Office Decoration'),
        ('12', 'Customer Service'),
        ('13', 'Cleaning and Maintenance'),
        ('14', 'Technology and Communication'),
        ('15', 'Marketing and Advertising'),
        ('16', 'Vehicle Expenses')
    ]

    name = models.CharField(
        max_length=250, primary_key=True, choices=EXPENSE_CATEGORY_CHOICES)

    def __str__(self):
        return self.name

 

class ExpenseSubCategory(models.Model):

    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Expense(models.Model):
    DIRECT_EXPENSE = 'Direct'
    DRAFT_EXPENSE = 'Draft'

    EXPENSE_CATEGORY_CHOICES = [
        (DIRECT_EXPENSE, 'Direct Expense'),
        (DRAFT_EXPENSE, 'Draft Expense'),
    ]

    date = models.DateField(null=True)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.SET_NULL, null=True, blank=True)
    expense_type = models.CharField(max_length=100)
    expense_category = models.CharField(max_length=10, choices=EXPENSE_CATEGORY_CHOICES)
    
    sub_category = models.ForeignKey(ExpenseSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    voucher_no = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_note = models.TextField(blank=True)
    def __str__(self):
        return f"Expense for {self.id} - {self.amount} - {self.date}"

class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# class Expense(models.Model):

#     expense_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Expense for {self.product.name}"


class Product(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    expense = models.ForeignKey(
        Expense, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.CharField(max_length=100)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    unit_measurement = models.CharField(max_length=100, null=True, blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_quantity = models.PositiveIntegerField()
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    stock_alert = models.PositiveIntegerField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_usage_maintenance_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    CONDITION_TYPES = [
        ('New', 'New'),
        ('Used', 'Used'),
        ('Expired', 'Expired'),
        ('Repaired', 'Repaired')
    ]
    condition = models.CharField(max_length=50, choices=CONDITION_TYPES)
    responsible_employee = models.CharField(max_length=100, blank=True)
    images = models.ImageField(upload_to='item_images/', blank=True, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True)

    qr_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if a WarehouseProduct with the same product already exists
        warehouse_product = WarehouseProduct.objects.filter(product=self).first()

        if warehouse_product:
            # WarehouseProduct already exists, increase the quantity
            warehouse_product.quantity += 1
            warehouse_product.save()
        else:
            # Create a new WarehouseProduct with the specified warehouse
            if self.warehouse:  # Assuming you have a 'warehouse' field in your Product model
                WarehouseProduct.objects.create(warehouse=self.warehouse, product=self, quantity=1)


class InventoryTransaction(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    TRANSACTION_TYPES = [
        ('Restock', 'Restock'),
        ('Usage', 'Usage'),
        ('Maintenance', 'Maintenance'),
        ('Fuel Refill', 'Fuel Refill'),
        ('Tire Replacement', 'Tire Replacement'),
        ('Cleaning', 'Cleaning'),
        ('Inventory Transfer', 'Inventory Transfer'),
        ('Damage Report', 'Damage Report'),
        ('Parts Ordering', 'Parts Ordering'),
        ('Parts Return', 'Parts Return'),
        ('Salvage or Disposal', 'Salvage or Disposal'),
        ('Audit or Inspection', 'Audit or Inspection'),
        ('Reservation', 'Reservation'),
        ('Loan or Borrow', 'Loan or Borrow'),
        ('Recall', 'Recall'),
        ('Installation or Assembly', 'Installation or Assembly'),
        # Add more transaction types as needed
    ]
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.item}"


# class Supplier(models.Model):
#     name = models.CharField(max_length=200)
#     supplier_code = models.CharField(max_length=20, null=True, blank=True)
#     address = models.CharField(max_length=250)
#     manager_name = models.CharField(max_length=50, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(max_length=200, blank=True, null=True)
#     address_street = models.CharField(max_length=100, blank=True, null=True)
#     address_city = models.CharField(max_length=50, blank=True, null=True)
#     address_state = models.CharField(max_length=50, blank=True, null=True)
#     address_postal_code = models.CharField(max_length=20, blank=True, null=True)
#     address_country = models.CharField(max_length=50, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     payment_history = models.TextField(blank=True)
#     contract_start_date = models.DateField(blank=True, null=True)
#     contract_end_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)
    supplier_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250)
    company = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address_street = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=50, blank=True, null=True)
    address_state = models.CharField(max_length=50, blank=True, null=True)
    address_postal_code = models.CharField(
        max_length=20, blank=True, null=True)
    address_country = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    account_name = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_account_no = models.CharField(max_length=150, null=True, blank=True)
    payment_history = models.TextField(blank=True)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class Biller(models.Model):
    name = models.CharField(max_length=200)
    biller_code = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address_country = models.CharField(max_length=50, blank=True, null=True)
    address_city = models.CharField(max_length=50, blank=True, null=True)
    nid = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    address_postal_code = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_account_no = models.CharField(max_length=150, null=True, blank=True)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name


# records the quantity of product in each warehouse
class WarehouseProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')




    

    

# records the transfer of each product

    
class Adjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('Addition', 'Addition'),
        ('Subtraction', 'Subtraction'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES)
    adjustment_date = models.DateField(null=True, blank=True)
    
    warehouse = models.CharField(max_length=100)  # Add this line for the warehouse field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type} {self.quantity} for {self.product} in {self.warehouse}"

    class Meta:
        ordering = ['-created_at']
class Purchase(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
      
        ('Canceled', 'Canceled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    order_tax =models.DecimalField(max_digits=10, decimal_places=2)
    order_discount =  models.CharField(max_length=12,blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')
    purchase_note = models.TextField(blank=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    reference_id = models.CharField(max_length=12, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Purchase #{self.id} ({self.purchase_date})"
    
    @property
    def used_product_quantity(self):
        # Calculate the used product quantity
        used_products = self.usedproduct_set.all()
        used_quantity = sum(used.quantity for used in used_products)
        return used_quantity
    
    @property
    def in_stock_quantity(self):
        return self.quantity - self.used_product_quantity
    
    def save(self, *args, **kwargs):
        # If the instance is being created for the first time, set the created_by field
        if not self.id and not self.created_by:
            # You'll need to set the created_by field based on your authentication mechanism
            # For example, you might get the current user from the request
            # Here, we assume you have a request object available
            current_user = self.request.user if hasattr(self, 'request') and self.request.user.is_authenticated else None

            self.created_by = current_user

        # Generate a unique identifier for reference_id with only numerical digits
        if not self.reference_id:
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            while Purchase.objects.filter(reference_id=f'IGL-{unique_id}').exists():
                unique_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            self.reference_id = f'IGL-{unique_id}'

        super().save(*args, **kwargs)

class WarehouseTransfer(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Complete', 'Complete'),
    ]
    source_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='source_transfers')
    destination_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='destination_transfers')
    transfer_date = models.DateField()  # This field should exist in the model
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='Pending')
    products = models.ManyToManyField(Product, through='TransferProduct')
    purchase=models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='transfered_product_purchases' ,null=True)


    tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100)
    attach_document = models.FileField(
        upload_to='transfer_documents/', null=True, blank=True)

    payment_note = models.TextField(blank=True)
    staff_remark = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.source_warehouse == self.destination_warehouse:
            raise ValidationError('Source and destination warehouses cannot be the same.')

    def __str__(self):
        return f"Transfer from {self.source_warehouse.name} to {self.destination_warehouse.name}"

class TransferProduct(models.Model):
    purchases=models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='transfered_product' ,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transfer = models.ForeignKey(WarehouseTransfer, on_delete=models.CASCADE, related_name='transfered_product')
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='from_warehouse')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='to_warehouse')
    transfer_date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name
    
    class Meta:
        unique_together = ('product', 'transfer')

class PurchaseInvoice(models.Model):
    invoice_date = models.DateField()
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    order_discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('Used', 'Used'),
        ('Not Used', 'Not Used'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Used')
    purchase_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.purchase.product.name


class ProductInstallation(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_item = models.ForeignKey(CategoryItem, on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    installation_note = models.CharField(max_length=500, null=True, blank=True)
    purchase_status = models.CharField(max_length=50, null=True, blank=True     )
    installation_date = models.DateField()

    def __str__(self):
        return self.purchase.product.name
    


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),

    ]
    
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20, default='Unpaid')


    cheque_number = models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=50, blank=True, null=True)

    def _str_(self):
        return f"Payment for Purchase #{self.purchase.id} ({self.payment_date})"


class PurchaseReturn(models.Model):
    purchase_return_date = models.DateField()
    reference = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    REMARK_CHOICES = [
        ('Date Expired', 'Date Expired'),
        ('N/A', 'N/A'),
        ('Duplicate', 'Duplicate'),
        ('Quality Less', 'Quality Less'),
        ('Not Good', 'Not Good'),
        ('Package Broken', 'Package Broken'),
        # Add more remarks as needed
    ]

    remark = models.CharField(
        max_length=50, choices=REMARK_CHOICES, blank=True, null=True)

    ACTION_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Completed', 'Completed'),
    ]
    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, default='Pending')
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return f"Purchase Return #{self.id} ({self.purchase_return_date})"


class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('purchase', 'Purchase Report'),
        ('payment', 'Payment Report'),
        ('product', 'Product Report'),
        ('stock', 'Stock Report'),
        ('warehouse', 'Warehouse Report'),
        ('supplier', 'Supplier Report'),
        ('tax', 'Tax Report'),
        ('shipping', 'Shipping Charge Report'),
    )

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.generated_at}"
