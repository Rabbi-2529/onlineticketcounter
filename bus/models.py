from django.db import models
from django.db.models import Q
# Create your models here.
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from datetime import date
from datetime import date, datetime
from django.conf import settings
import itertools
import uuid
import os
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from .root_permissions import root_user_group_permissions


def profile_picture_upload(instance, filename):
    return os.path.join('profile_pictures', filename)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, 'Root'),
        (1, "Company"),
        (2, "Staff"),
        (3, "Users"),
    )

    user_id = models.IntegerField(max_length=100, unique=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    phone_number = models.CharField(max_length=500)
    nid_number = models.CharField(max_length=100, blank=True)
    city_name = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    nid_image = models.ImageField(upload_to='nid_images', blank=True)
    address = models.TextField(blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        upload_to='profile_pictures', blank=False)
    staff_type = models.ForeignKey('StaffType', on_delete=models.SET_NULL, null=True, blank=True)


    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='custom_users', blank=True, null=True)

    def is_online(self):
        now = timezone.now()
        # Assuming the user is online if they have been active in the last 5 minutes
        return now - self.last_active < timezone.timedelta(minutes=5)

    def save(self, *args, **kwargs):
        if not self.user_id:
            # find the last user
            last_user = CustomUser.objects.order_by('-user_id').first()

            if last_user:
                last_user_id = int(last_user.user_id)

                if str(last_user_id).startswith('445') and len(str(last_user_id)) >= 6:
                    # Ensure at least 6 digits
                    new_user_id_str = str(last_user_id + 1).zfill(6)
                    new_user_id = int(new_user_id_str)
                else:
                    new_user_id = 445002

            else:
                new_user_id = 445001

            self.user_id = new_user_id

        if not self.username or self.username == 'None':
            self.username = str(new_user_id)

        super(CustomUser, self).save(*args, **kwargs)

        if self.user_type == 0 and not hasattr(self, 'rootuser'):
            root_user = RootUser.objects.filter(email=self.email).first()

            root_user_group, _ = Group.objects.get_or_create(
                name='root_user_group')

            # Fetch permissions by codename and add them to the group's permissions
            for codename in root_user_group_permissions:
                permission = Permission.objects.get(codename=codename)
                root_user_group.permissions.add(permission)

            self.groups.add(root_user_group)

            for permission in root_user_group.permissions.all():
                # Assign the permission to the user
                self.user_permissions.add(permission)

            if not root_user:
                RootUser.objects.create(
                    custom_user=self, username=self.username, email=self.email)

        elif self.user_type == 1:
            # admin_user = Company.objects.filter(root_user=self).first()
            super_admin_group, created_at = Group.objects.get_or_create(
                name='Super Admins')
            permissions_to_include = Permission.objects.exclude(
                codename__in=['add_company', 'change_company', 'delete_company', 'view_company'])

            self.groups.add(super_admin_group)
            self.user_permissions.set(permissions_to_include)

class StaffType(models.Model):
    STAFF_TYPE_CHOICES = [
        ('Inventory', 'Inventory'),
        ('Accounts', 'Accounts'),
        ('HR', 'HR'),
        ('Software Engineer', 'Software Engineer'),
        ('Employee', 'Employee'),
    ]

    name = models.CharField(
        max_length=20,
        choices=STAFF_TYPE_CHOICES,
        primary_key=True,
    )
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
class Company(models.Model):
    name = models.CharField(max_length=100)
    company_id = models.CharField(max_length=100, unique=True)
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50,)
    root_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_suspended = models.BooleanField(default=False)
    staff_types = models.ManyToManyField(StaffType)  # Define the ManyToMany relationship here

      # Add a field to indicate if the company is suspended

    def __str__(self):
        return str(self.company_id)
    
    def save(self, *args, **kwargs):
        if not self.company_id:
            # Generate the last 6 digits of the ID
            last_six_digits = str(Company.objects.count() + 1).zfill(6)
            self.company_id = f'4459{last_six_digits}'
        super().save(*args, **kwargs)

    def suspend(self):
        self.is_suspended = True
        self.save()

    def unsuspend(self):
        self.is_suspended = False
        self.save()


class PermissionCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class RootUser(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=5, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=500, blank=True, null=True)
    # def save(self, *args, **kwargs):
    #     super(RootUser, self).save(*args, **kwargs)
    #     self.groups.add(root_user_group)

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)

    #     root_user_group, _ = Group.objects.get_or_create(name='root_user_group')
    #     root_user_group.permissions.add(*root_user_group_permissions)
    #     self.groups.add(root_user_group)


class CustomPermission(models.Model):
    category = models.ForeignKey(PermissionCategory, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)  # Change this to ManyToManyField

    def __str__(self):
        return self.category.name




class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    staff_type = models.ForeignKey(
        StaffType, on_delete=models.SET_NULL, null=True)
  
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def total_ticket_bookings(self):
        coach_ids = Coach.objects.filter(
            staff=self).values_list('id', flat=True)
        return Booking.objects.filter(coach_id__in=coach_ids).count()


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.ForeignKey(
        'Company', on_delete=models.CASCADE, related_name='users', blank=True, null=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Customers(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    id_type = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.first_name or ''


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "1":
            Company.objects.create(root_user=instance)
        elif instance.user_type == "2":
            Staffs.objects.create(admin=instance, address="")
        elif instance.user_type == 3:
            Users.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "1":
        instance.company.save()
    elif instance.user_type == "2":
        instance.staffs.save()
    elif instance.user_type == 3:
        instance.users.save()




class Visitor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.CharField(max_length=15)
    date_visited = models.DateTimeField(auto_now_add=True)
    page_visited = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)


class TicketBooking(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    seats = models.CharField(max_length=200)
    total_price = models.IntegerField()
    reservation_date = models.DateTimeField(auto_now_add=True)
    boarding_point = models.CharField(max_length=200)

    def __str__(self):
        return self.boarding_point


class Division(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Upazila(models.Model):
    name = models.CharField(max_length=150)
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Thana(models.Model):
    name = models.CharField(max_length=150)
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Union(models.Model):
    name = models.CharField(max_length=150)
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)
    upazila = models.ForeignKey(
        Upazila, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Counter(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=150, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_account_no = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True)
    union = models.ForeignKey(
        Union, on_delete=models.CASCADE, null=True, blank=True)
    thana = models.ForeignKey(
        Thana, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField()
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True,default=0, verbose_name='Credit Card Balance')
    phone_numbers = models.TextField()
    def get_phone_numbers(self):
        return self.phone_numbers.split('\n')
    def get_address(self):
        return self.address.split('\n')
    def __str__(self):
        return self.name
    


class BusStop(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='bus_stops')

    def __str__(self):
        return self.name.name
    
    def save(self, *args, **kwargs):
        existing_stop = BusStop.objects.filter(company=self.company, name=self.name).exclude(id=self.id).first()

        if existing_stop:
            raise ValidationError('A record with the same journey_date already exists.')
        
        super().save(*args, **kwargs)
        


class Route(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_point = models.ForeignKey(
        BusStop, on_delete=models.CASCADE, related_name='start_routes'
    )
    end_point = models.ForeignKey(
        BusStop, on_delete=models.CASCADE, related_name='end_routes'
    )
    intermediate_stops = models.ManyToManyField(
        BusStop, blank=True, related_name='intermediate_routes'
    )
    distance = models.IntegerField()
    travel_time = models.DurationField()

    def __str__(self):
        return f"{self.start_point} - {self.end_point}"

    def travel_time_hours_minutes(self):
        hours, remainder = divmod(self.travel_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours} hours, {minutes} minutes"

    @property
    def split_into_parts(self):
        stops = [self.start_point.name] + \
                [stop.name for stop in self.intermediate_stops.all()] + \
                [self.end_point.name]
        return stops


class Tax(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    TAX_STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Disabled'),
    ]

    tax_name = models.CharField(max_length=100)
    tax_value = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Enter the tax value as a percentage.")
    tax_number = models.CharField(max_length=10, unique=True)
    status = models.IntegerField(choices=TAX_STATUS_CHOICES, default=1)

    def __str__(self):
        return self.tax_name


class PaymentMethod(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.name


class PropularRoutes(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    fromdescription = models.CharField(max_length=2000)
    todescription = models.CharField(max_length=2000)
    # coach = models.ForeignKey(Coach, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.route}"


class contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    phonenumber = models.IntegerField()


class feedback(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    email = models.EmailField(max_length=400)
    mobile = models.CharField(max_length=400)
    subject = models.TextField()
    details = models.TextField()


class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class TermsAndConditions(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()


class Profile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    STATE_CHOICES = (

        ('DH', 'Dhaka'),
        ('CTG', 'Chittagong'),
        ('RS', 'Rajshahi'),
        ('KH', 'Khulna'),
        ('SYL', 'Sylhet'),
        ('BAR', 'Barisal'),

    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures', null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    nid = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    postcode = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(
        max_length=255, choices=STATE_CHOICES, null=True, blank=True)


def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Complaint(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    APPLICATION_CHOICES = [
        ('GENERAL', 'General'),
        ('BUS', 'Bus Service'),

    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    application = models.CharField(max_length=50, choices=APPLICATION_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.title


class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    regi_number = models.CharField(max_length=20, unique=True)
    fleet_type = models.CharField(max_length=20)
    eng_number = models.CharField(max_length=20)
    model_name = models.CharField(max_length=100)
    chassis_number = models.CharField(max_length=50)
    driver_number = models.CharField(max_length=20)

    def __str__(self):
        return self.number


class BusFitness(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fitness_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=20)
    fitness_start_date = models.DateField()
    fitness_end_date = models.DateField()
    start_mileage = models.PositiveIntegerField()
    end_mileage = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.vehicle.regi_number} - {self.fitness_name}"


class Bus(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    BUS_TYPE_CHOICES = [
        ('CC', 'Chair Coach'),
        ('SIP', 'Sleeping Coach'),
        ('DD', 'Double Decker'),
    ]
    EXTRA_SEAT_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    NUMBER_OR_COLUMN_CHOICES = [
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
    ]
    CLASS_TYPE_CHOICES = (
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    )
    bus_type = models.CharField(max_length=10, choices=BUS_TYPE_CHOICES)
    number_or_column = models.CharField(
        max_length=2, choices=NUMBER_OR_COLUMN_CHOICES)
    bus_number = models.CharField(max_length=20)
    seat_type_1 = models.CharField(max_length=20, blank=True)
    seat_type_2 = models.CharField(max_length=20, blank=True)
    seat_type_3 = models.CharField(max_length=20, blank=True)
    extra_seat = models.IntegerField(
        choices=EXTRA_SEAT_CHOICES, blank=True, null=True)
    total_seats = models.IntegerField()
    class_type = models.CharField(max_length=10, choices=CLASS_TYPE_CHOICES)
    def __str__(self):
        return self.bus_number


class JourneyDateHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    journey_date = models.DateField(null=True, blank=True)
    upcoming_schedule = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.journey_date}"

    def is_upcoming_journey(self):
        return self.journey_date >= date.today()


class Facility(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BoardingPoint(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='boarding_points'
    )
    point_name = models.CharField(max_length=200)

    def __str__(self):
        return self.point_name


class Coach(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        null=True
    )
    routes = models.ManyToManyField(Route)

    journey_dates = models.ManyToManyField(JourneyDateHistory, null=True)
    coachnumber = models.IntegerField()
    coachtype = models.CharField(max_length=300, verbose_name='Type')
    coachmodelname = models.CharField(max_length=400, verbose_name='Model')
    is_marked = models.BooleanField(default=False)

    arrivaltime = models.TimeField(
        verbose_name='Arv.Time', auto_now=False, auto_now_add=False
    )
    depraturetime = models.TimeField(
        verbose_name='Dep.Time',
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )

    returndate = models.DateField(null=True, blank=True)

    cancellation_policy = models.TextField(
        default='We Provide You All TLD Domain Services In Low Cost. Just you can make an order using our online billing, we will activate your domain within a few minutes.', editable=True, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    boarding_points = models.ManyToManyField(
        BoardingPoint, null=True, blank=True)
    staffs = models.ManyToManyField(Staffs, related_name='coaches', blank=True)

    def __str__(self):
        return f"{self.coachnumber}"

    @property
    def recent_upcoming_scheduled(self):
        today = date.today()
        first_valid_journey_date = self.journey_dates.filter(
            journey_date__gte=today).earliest('journey_date')
        return first_valid_journey_date if first_valid_journey_date else None

    def update_journey_date(self, new_journey_date):
        self.journeydate = new_journey_date
        self.save()

    def update_return_date(self, new_return_date):
        self.returndate = new_return_date
        self.save()

    # def coach_journey_date(self, target_date):
    #     journey_date = self.journey_dates.filter(target_date)


class RoutePart(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name='parts')
    start_point = models.ForeignKey(
        BusStop, on_delete=models.CASCADE, related_name='start_route_parts'
    )
    end_point = models.ForeignKey(
        BusStop, on_delete=models.CASCADE, related_name='end_route_parts'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    coach = models.ForeignKey(
        Coach, on_delete=models.CASCADE, related_name='route_parts'
    )

    def _str_(self):
        return f"{self.start_point.name} -> {self.end_point.name} ({self.coach})"

    @property
    def is_special_routepart(self):
        return self.route.start_point == self.start_point and self.route.end_point == self.end_point


class Seat(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    SEAT_TYPE_CHOICES = [
        ('seat_type_1', '1:1'),
        ('seat_type_2', '1:2'),
        ('seat_type_3', '2:2'),
        ('mixed', 'Mixed (1:1 + 1:2 + 2:2)'),
    ]

    bus = models.ForeignKey(
        Bus, on_delete=models.CASCADE, related_name='seats')
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPE_CHOICES)
    row_number = models.PositiveIntegerField()
    seat_number = models.CharField(max_length=2)

    def __str__(self):
        return f'Seat - Bus: {self.bus.bus_number}, Row: {self.row_number}, Seat: {self.seat_number}'

    def save(self, *args, **kwargs):
        if self.bus:
            if self.seat_type == 'seat_type_1':
                self.seat_type = self.bus.seat_type_1
            elif self.seat_type == 'seat_type_2':
                self.seat_type = self.bus.seat_type_2
            elif self.seat_type == 'seat_type_3':
                self.seat_type = self.bus.seat_type_3
            elif self.seat_type == 'mixed':
                self.seat_type = f"{self.bus.seat_type_1} + {self.bus.seat_type_2} + {self.bus.seat_type_3}"
            self.row_number = self.bus.number_or_column
            self.seat_number = str(self.bus.total_seats)
        super().save(*args, **kwargs)


class Booking(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    route_part = models.ForeignKey(RoutePart, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, null=True, blank=True)
    seat_number = models.CharField(max_length=10)
    price = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    journey_date = models.ForeignKey(
        JourneyDateHistory,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True  
    )
    pnr = models.CharField(max_length=8, unique=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Booking #{self.id} - User: {self.user.username}" or ''

    @classmethod
    def get_booked_seats(cls, journey_date, coach, company):
  
        booked_seat_numbers = set()


        booked_seats = cls.objects.filter(
            journey_date=journey_date, coach=coach, is_booked=True
        )


        special_booked_seats = set()
        non_special_booked_seats = set()

        for booked_seat in booked_seats:

            booked_seat_list = str(booked_seat.seat_number).split()
            booked_seat_numbers.update(booked_seat_list)


            if booked_seat.route_part.is_special_routepart:
                special_route = booked_seat.route_part.route
                special_route_parts = RoutePart.objects.filter(
                    route=special_route)
                for part in special_route_parts:
                    if part != booked_seat.route_part:
                        special_booked_seats_other_part = cls.objects.filter(
                            journey_date=journey_date,
                            coach=coach,
                            route_part=part,
                            is_booked=True,
                        )
                        for special_booking in special_booked_seats_other_part:
                            booked_seat_list = str(
                                special_booking.seat_number).split()
                            special_booked_seats.update(booked_seat_list)
            else:

                non_special_booked_seats.add(booked_seat.seat_number)

        total_seats = coach.bus.total_seats
        total_booked_seats = len(booked_seat_numbers)
        remaining_seats = total_seats - total_booked_seats
        return total_seats, remaining_seats

    def set_booking_status(self):
        if not self.is_paid:
            self.status = 'Booked'
        elif self.route_part.depraturetime and datetime.now() > datetime.combine(self.journey_date.journey_date, self.route_part.depraturetime):
            self.status = 'Expired'
        elif self.is_paid:
            self.status = 'Paid'
        elif self.cancelticket_set.filter(status='Approved').exists():
            self.status = 'Canceled'

    def save(self, *args, **kwargs):

        if self.route_part.is_special_routepart and not self.is_booked:

            other_route_parts = RoutePart.objects.exclude(
                pk=self.route_part.pk)
            bookings_to_update = Booking.objects.filter(
                coach=self.coach,
                seat_number=self.seat_number,
                journey_date=self.journey_date,
                route_part__in=other_route_parts,
            )
            for booking in bookings_to_update:
                booking.is_booked = True
                booking.save()

        super(Booking, self).save(*args, **kwargs)


class Click(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f"Click by {self.user.username} on {self.date}"


class CancelTicket(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    cancel_fee = models.DecimalField(
        max_digits=10, decimal_places=2) 
    payment_type = models.CharField(max_length=50)  
    payment_details = models.TextField() 

    def _str_(self):
        return f"CancelTicket for {self.booking.pnr}"

    def refund_booking(self, booking):

        booking.is_paid = False
        booking.save()

    def save(self, *args, **kwargs):

        if self.status == 'Approved' and self.booking:

            with transaction.atomic():

                self.refund_booking(self.booking)

        super().save(*args, **kwargs)


class PopupDuration(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    duration_minutes = models.PositiveIntegerField(
        help_text="Duration in minutes")

    def _str_(self):
        return self.duration_minutes


class Refund(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    refund_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    refund_reason = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Refund for Booking #{self.booking.pk}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_approved and not self.booking.is_paid:

            self.booking.is_paid = False
            self.booking.save()
        elif not self.is_approved and self.booking.is_paid:

            self.booking.is_paid = True
            self.booking.save()

class Payment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Unpaid')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment for Booking #{self.booking.pk}"

    def save(self, *args, **kwargs):
        total_amount = Decimal(str(self.booking.price))  # Convert to Decimal
        total_paid = Payment.objects.filter(booking=self.booking).aggregate(
            Sum('amount_paid'))['amount_paid__sum'] or Decimal('0.00')  # Convert to Decimal

        print(f'Total Paid: {total_paid}')
        print(f'Total Amount: {total_amount}')

        if total_paid is None or total_paid == Decimal('0.00'):
            self.payment_status = 'Unpaid'
        elif total_paid == total_amount:
            
            self.payment_status = 'Paid'

            self.booking.is_paid = True
            self.booking.save()
        elif total_paid < total_amount:
            self.payment_status = 'Partial'
        else:
            self.payment_status = 'Unknown'

        super().save(*args, **kwargs)


