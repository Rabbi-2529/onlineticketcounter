from django.apps import AppConfig


class BusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bus'

    
def ready(self):
        # Start the scheduler when the Django application is ready
        from bus.scheduler import start_scheduler
        start_scheduler()