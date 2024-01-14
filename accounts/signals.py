from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Bank, BalanceTransfer, FinancialTransaction, PaymentInvoice, CreditVoucher, DebitVoucher, Bill
from .models import Notification

@receiver(post_save, sender=Bank)
@receiver(post_save, sender=BalanceTransfer)
@receiver(post_save, sender=FinancialTransaction)
@receiver(post_save, sender=PaymentInvoice)
@receiver(post_save, sender=CreditVoucher)
@receiver(post_save, sender=DebitVoucher)
@receiver(post_save, sender=Bill)
def create_notification(sender, instance, created, **kwargs):
    if created:
        model_name = ContentType.objects.get_for_model(instance).model
        notification_message = f"New {model_name} added: {instance}."

        # Try to get the user associated with the instance dynamically
        if hasattr(instance, 'user'):
            recipient_user = instance.user
        elif hasattr(instance, 'get_user'):  # For example, if there's a method to get the user
            recipient_user = instance.get_user()
        else:
            # If no user association is found, you need to adjust this part based on your actual models
            recipient_user = None

        # Create the notification with the recipient user if available
        if recipient_user:
            Notification.objects.create(message=notification_message, recipient=recipient_user)
