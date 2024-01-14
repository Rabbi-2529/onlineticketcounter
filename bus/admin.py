from django.contrib import admin
from django.urls import reverse
from django.contrib.admin import SimpleListFilter
from datetime import date
from datetime import date, datetime

from django.utils.html import format_html
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple



from django.contrib.auth.admin import UserAdmin

from bus.models import CustomUser, TicketBooking, Coach, Route, PropularRoutes, Counter, District, feedback, Category, FAQ, TermsAndConditions, Profile, Complaint, Bus, Seat, Booking, BoardingPoint, JourneyDateHistory, CancelTicket, BusStop, RoutePart, Division, District, Upazila, Union, CustomPermission, PermissionCategory, PopupDuration, Payment, Customers, Company, Staffs, StaffType, RootUser, PaymentMethod


class UserModel(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, UserModel)


class TicketBookingAdmin(admin.ModelAdmin):
    list_display = ('boarding_point', 'seats', 'total_price',)

    # search_fields = ('name', 'phone')


admin.site.register(TicketBooking, TicketBookingAdmin)


class CoachAdmin(admin.ModelAdmin):
    list_display = ('coachnumber', 'bus',  'coachtype', 'coachmodelname',
                    'arrivaltime', 'depraturetime', 'returndate', 'cancellation_policy')
    list_filter = ('bus',)
    search_fields = ('bus__bus_number', 'coachnumber')
    autocomplete_fields = ('bus',)


class BusStopAdmin(admin.ModelAdmin):
    list_display = ('get_district_name',)

    def get_district_name(self, obj):
        return obj.name.name if obj.name else None

    get_district_name.short_description = 'District Name'


class RoutePartInline(admin.TabularInline):
    model = RoutePart
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    inlines = [RoutePartInline]
    list_display = ('id', 'display_start_point', 'display_end_point', 'distance',
                    'travel_time_hours_minutes', 'show_split_parts')
    filter_horizontal = ('intermediate_stops',)
    readonly_fields = ('show_split_parts', 'travel_time_hours_minutes')

    def travel_time_hours_minutes(self, obj):
        hours, remainder = divmod(obj.travel_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours} hours, {minutes} minutes"

    travel_time_hours_minutes.short_description = 'Travel Time'

    def show_split_parts(self, obj):
        return obj.split_into_parts

    show_split_parts.short_description = 'Split Parts'

    def display_start_point(self, obj):
        return str(obj.start_point.name.name) if obj.start_point and obj.start_point.name else ''
    display_start_point.short_description = 'Start Point'

    def display_end_point(self, obj):
        return str(obj.end_point.name.name) if obj.end_point and obj.end_point.name else ''
    display_end_point.short_description = 'End Point'


admin.site.register(Route, RouteAdmin)
admin.site.register(BusStop, BusStopAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile']


admin.site.register(feedback, FeedbackAdmin)


class PopularRoutesAdmin(admin.ModelAdmin):
    list_display = ('route', 'fromdescription', 'todescription')


admin.site.register(PropularRoutes, PopularRoutesAdmin)


class CounterInline(admin.StackedInline):
    model = Counter


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['get_district_name']

    def get_district_name(self, obj):
        return obj.name

    get_district_name.short_description = 'Name'

    inlines = [CounterInline]


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'phone_numbers', 'district']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender')




admin.site.register(Profile, ProfileAdmin)


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus_type', 'bus_number')
    list_filter = ('bus_type',)
    search_fields = ('bus_number',)
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('bus', 'seat_type', 'row_number', 'seat_number')
    list_filter = ('bus', 'seat_type')
    search_fields = ('bus__bus_number', 'row_number', 'seat_number')


class JourneyDateFilter(SimpleListFilter):
    title = 'Journey Date'
    parameter_name = 'journeydate'

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        dates = queryset.order_by('journey_date').values_list(
            'journey_date', flat=True).distinct()

        # Convert values to date objects
        valid_dates = []
        for date_value in dates:
            try:
                valid_date = datetime.strptime(
                    str(date_value), '%Y-%m-%d').date()
                valid_dates.append(valid_date)
            except ValueError:
                # Handle invalid date values
                pass

        return [(date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')) for date in valid_dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(journey_date=self.value())


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'coach', 'seat_number', 'price', 'journey_date', 'route_part_info', 'is_booked', 'seat_plan_link', 'pnr'
    )
    list_filter = ('user', 'coach__coachnumber',
                   JourneyDateFilter, 'is_booked')
    search_fields = ('user_username', 'coach_coachmodelname',
                     'coach_journeydate', 'route_partcoachroute_name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Fetch related 'coach' and 'route_part' objects efficiently
        queryset = queryset.select_related('coach', 'route_part')
        return queryset

    def journey_date(self, obj):
        return obj.coach.journeydate

    journey_date.admin_order_field = 'coach__journeydate'
    journey_date.short_description = 'Journey Date'

    def route_part_info(self, obj):
        if obj.route_part:
            return f"From: {obj.route_part.start_point}, To: {obj.route_part.end_point}"
        return "N/A"
    route_part_info.short_description = 'Route Part'

    def seat_plan_link(self, obj):
        journey_date = obj.coach.journey_dates
        url = reverse('admin:bus_seat_changelist') + \
            f'?journeydate={journey_date}'
        return format_html('<a href="{}">View Seat Plan</a>', url)

    seat_plan_link.short_description = 'Seat Plan'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "coach":
            # Get the journey_date from the request parameters
            journey_date_str = request.GET.get('journey_date')
            if journey_date_str:
                try:
                    journey_date = datetime.strptime(
                        journey_date_str, '%d-%m-%Y').date()
                except ValueError:
                    # Handle invalid date format gracefully
                    raise ValueError(
                        "Invalid journey_date format. Use 'DD-MM-YYYY'.")
            else:
                journey_date = None

            # Filter coach choices based on journey_date
            if journey_date:
                kwargs["queryset"] = Coach.objects.filter(
                    journeydate=journey_date)
            else:
                kwargs["queryset"] = Coach.objects.none()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CancelTicketAdmin(admin.ModelAdmin):
    readonly_fields = ('booking', 'created_at')
    list_display = ('booking', 'get_created_at', 'get_status')
    list_filter = ('status',)

    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'

    def get_status(self, obj):
        return obj.status
    get_status.short_description = 'Status'


class PermissionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CustomPermissionAdminForm(forms.ModelForm):
    class Meta:
        model = CustomPermission
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple('Permissions', is_stacked=False),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Get all available permissions
        self.fields['permissions'].queryset = Permission.objects.all()


class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('category',)  # Removed 'permissions' from list_display
    form = CustomPermissionAdminForm


admin.site.register(PermissionCategory, PermissionCategoryAdmin)
admin.site.register(CustomPermission, CustomPermissionAdmin)


admin.site.register(CancelTicket, CancelTicketAdmin)


admin.site.site_header = 'Bus Admin'
admin.site.site_title = 'Bus Admin'
admin.site.register(Booking, BookingAdmin)
admin.site.register(BoardingPoint)
admin.site.register(JourneyDateHistory)
admin.site.register(RoutePart)
admin.site.register(Division)
admin.site.register(Upazila)
admin.site.register(Union)
admin.site.register(Permission)
admin.site.register(PopupDuration)
admin.site.register(Payment)
admin.site.register(Customers)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'name', 'user_name',
                    'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'user_name')


admin.site.register(Staffs)
admin.site.register(StaffType)
admin.site.register(RootUser)
admin.site.register(PaymentMethod)

