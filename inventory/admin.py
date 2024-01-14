from django.contrib import admin
from inventory.models import *
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
# Define your TransferItemForm here if it's not already defined in forms.py


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass  # Customize the admin options for SubCategory if needed


@admin.register(CategoryItem)
class CategoryItemAdmin(admin.ModelAdmin):
    pass  # Customize the admin options for CategoryItem if needed


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass  # Customize the admin options for Product if needed


class WarehouseTransferForm(ModelForm):
    class Meta:
        model = WarehouseTransfer
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        source_warehouse = cleaned_data.get('source_warehouse')
        destination_warehouse = cleaned_data.get('destination_warehouse')

        if source_warehouse == destination_warehouse:
            raise ValidationError(
                "Source and destination warehouses cannot be the same.")


@admin.register(WarehouseTransfer)    
class WarehouseTransferAdmin(admin.ModelAdmin):
    form = WarehouseTransferForm
    list_display = ('source_warehouse', 'destination_warehouse',
                    'transfer_date', 'status')
    list_filter = ('source_warehouse', 'destination_warehouse', 'status')


admin.site.register(Warehouse)

admin.site.register(Purchase)
admin.site.register(Payment)
admin.site.register(PurchaseReturn)
admin.site.register(WarehouseProduct)
admin.site.register(TransferProduct)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(UnitOfMeasurement)
admin.site.register(PurchaseInvoice)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSubCategory)
admin.site.register(Adjustment)
admin.site.register(Expense)
admin.site.register(Biller)