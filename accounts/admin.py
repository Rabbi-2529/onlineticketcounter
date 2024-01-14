from django.contrib import admin
from accounts.models import FinancialTransaction,Bank,CreditVoucher,DebitVoucher,PaymentInvoice,Bill,Notification,JournalEntry
admin.site.register(FinancialTransaction)
admin.site.register(Bank)
admin.site.register(CreditVoucher)
admin.site.register(DebitVoucher)
admin.site.register(PaymentInvoice)
admin.site.register(Bill)
admin.site.register(Notification)
admin.site.register(JournalEntry)