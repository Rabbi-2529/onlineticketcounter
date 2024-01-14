from .models import Visitor
from django.contrib.auth import get_user_model
from datetime import datetime
from . models import Visitor
from django.utils import timezone

User = get_user_model()


class VisitorsMiddleware:
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        # Process unauthenticated visitors
        if not request.user.is_authenticated:
            visitor, created = Visitor.objects.get_or_create(
                ip_address=ip_address)
            visitor.date_visited = datetime.now()  # Use datetime instead of now()
            visitor.save()


class UserLastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Update the last_active field to the current time
            request.user.last_active = timezone.now()
            request.user.save()

        return response
