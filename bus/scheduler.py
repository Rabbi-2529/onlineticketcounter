# bus/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta, date
from bus.models import Booking, JourneyDateHistory
import logging

def update_bookings():
    try:
        current_time = timezone.localtime(timezone.now())
        current_date = date.today()
        journey_date = JourneyDateHistory.objects.get(journey_date=current_date)
        one_hour_delta = timedelta(hours=1)
        bookings_to_update = Booking.objects.filter(
            coach__depraturetime__lt=current_time + one_hour_delta, is_booked=True, is_paid=False, journey_date=journey_date
        )
        print('bookings_to_update: ', bookings_to_update)
        print('journey_date schedule: ', journey_date)

        for booking in bookings_to_update:
            booking.is_booked = False
            booking.save(update_fields=['is_booked'])
        
        print('Booking status updated')
    except Exception as e:
        logging.exception("An error occurred while updating bookings: %s", str(e))

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the update_bookings function to run every minute (adjust as needed)
    scheduler.add_job(update_bookings, 'interval', seconds=10)
    scheduler.start()
