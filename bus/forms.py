from django import forms
from django.forms import ChoiceField
from django.core.validators import RegexValidator
from bus.models import Customers, TicketBooking, Profile, Complaint, Bus, Booking, CustomUser

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass
class DateInput(forms.DateInput):
    input_type = "date"

# class AddCustomerForm(forms.Form):
#     email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
#     password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
#     first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
#     address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     phone=forms.CharField(label="Phone",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))


#     gender_choice=(
#         ("Male","Male"),
#         ("Female","Female")
#     )


#     sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))

#     profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

# class EditCustomerForm(forms.Form):
#     email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
#     first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
#     address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))


#     gender_choice=(
#         ("Male","Male"),
#         ("Female","Female")
#     )


#     sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))

#     profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)

class ReservationForm(forms.ModelForm):
    class Meta:
        model = TicketBooking
        fields = ['boardingpoint', 'seats', 'total']

    boardingpoint = forms.ChoiceField(label='Boarding point', choices=[('131390982', 'Abdullahpur Bus Point (09:30 PM)'),
                                                                       ('131390986', 'BNS Center, Azampur, Uttara (09:35 PM)'),
                                                                       ('131390987',
                                                                        'Airport Bus Point (09:45 PM)'),
                                                                       ('131390979',
                                                                        'Khilkhet (09:50 PM)'),
                                                                       ('131390991',
                                                                        'Jamuna Future Park (10:05 PM)'),
                                                                       ('131390988',
                                                                        'Norda (10:15 PM)'),
                                                                       ('131390989',
                                                                        'Badda Bus Stand (10:30 PM)'),
                                                                       ('131390990',
                                                                        'Rampura (10:40 PM)'),
                                                                       ('131390983',
                                                                        'Fakirapole (10:50 PM)'),
                                                                       ('131390981', 'Arambag Bus Point (11:15 PM)')])
    seats = forms.CharField(widget=forms.HiddenInput())
    total = forms.DecimalField(widget=forms.HiddenInput())


class ProfileForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^01[3-9]\d{8}$',
        message='Phone number must be 11 digits and starting with valid formet '
    )

    # NID validator function
    def validate_nid(nid):

        if len(nid) != 10:
            raise forms.ValidationError('NID must be 10 digits')

        # NID must contain only digits
        if not nid.isdigit():
            raise forms.ValidationError('NID must contain only digits')

        # Additional validation rules...

    # Define the form fields and apply validators
    mobile_number = forms.CharField(validators=[phone_regex])
    nid = forms.CharField(validators=[validate_nid])

    class Meta:
        model = Profile
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'mobile_number',
            'address',
            'nid',
            'date_of_birth',
            # 'gender',
            'postcode',
            'state',
        ]
        labels = {
            'profile_picture': 'Profile Picture',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'mobile_number': 'Mobile Number',
            'address': 'Address',
            'nid': 'NID',
            'date_of_birth': 'Date of Birth',
            # 'gender': 'Gender',
            'postcode': 'Postcode',
            'state': 'State',
        }
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'nid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NID No.'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date'}),
            # 'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip/Postal Code'}),
            'state': forms.Select(attrs={'class': 'form-control', 'placeholder': 'State/City'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['profile_picture'].required = False


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'application', 'description']


class BusRegistrationForm(forms.ModelForm):
    extra_seat = forms.ChoiceField(
        choices=Bus.EXTRA_SEAT_CHOICES, required=False)
    number_or_column = forms.ChoiceField(
        choices=Bus.NUMBER_OR_COLUMN_CHOICES, required=False)
    class_type = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Bus.CLASS_TYPE_CHOICES)
    class Meta:
        model = Bus
        exclude = ['company']
        # fields = '__all__'
        labels = {
            'bus_type': 'Bus Type',
            'number_or_column': 'Number or Column',
            'bus_number': 'Bus Number',
            'seat_type_1': 'Seat Type 1',
            'seat_type_2': 'Seat Type 2',
            'seat_type_3': 'Seat Type 3',
            'extra_seat': 'Extra Seat',
            'total_seats': 'Total Seats',
            'class_type': 'Class Type',
        }
    def clean(self):
        cleaned_data = super().clean()
        seat_type_1 = cleaned_data.get('seat_type_1')
        seat_type_2 = cleaned_data.get('seat_type_2')
        seat_type_3 = cleaned_data.get('seat_type_3')
        number_or_column = cleaned_data.get('number_or_column')
        extra_seat = cleaned_data.get('extra_seat')
        # # if seat_type_1 == number_or_column and seat_type_2 != '0':
        # #     self.add_error(
        # #         'seat_type_2', "If seat_type_1 is equal to number_or_column, seat_type_2 must be 0.")
        # if seat_type_2 == number_or_column and seat_type_1 != '0':
        #     self.add_error(
        #         'seat_type_1', "If seat_type_2 is equal to number_or_column, seat_type_1 must be 0.")
        # if seat_type_3 == number_or_column and (seat_type_1 != '0' or seat_type_2 != '0'):
        #     self.add_error(
        #         None, "If seat_type_3 is equal to number_or_column, seat_type_1 and seat_type_2 must be 0.")
        # Calculate total seats
        if number_or_column and seat_type_1 and seat_type_2 and seat_type_3:
            total_seats = int(seat_type_1) + \
                int(seat_type_2) + int(seat_type_3)
            cleaned_data['total_seats'] = total_seats
        # Update cleaned_data with modified seat type values
        if extra_seat == '1':
            cleaned_data['extra_seat'] = 1
        else:
            cleaned_data['extra_seat'] = 0
        cleaned_data['seat_type_1'] = seat_type_1
        cleaned_data['seat_type_2'] = seat_type_2
        cleaned_data['seat_type_3'] = seat_type_3
        # Auto-add bus number if two numbers are given
        if number_or_column and number_or_column.isdigit():
            bus_number = cleaned_data.get('bus_number')
            if bus_number and bus_number.isdigit():
                cleaned_data['bus_number'] = bus_number + \
                    '-' + number_or_column
        return cleaned_data

# class BusRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Bus
#         fields = '__all__'
#         labels = {
#             'bus_type': 'Bus Type',
#             'class_type': 'Type',
#             'number_or_column': 'Number or Column',
#             'bus_number': 'Bus Number',
#             'seat_type_1': 'Seat Type 1',
#             'seat_type_2': 'Seat Type 2',
#             'seat_type_3': 'Seat Type 3',

#             'extra_seat': 'Extra Seat',
#             'total_seats': 'Total Seats',
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         seat_type_1 = cleaned_data.get('seat_type_1')
#         seat_type_2 = cleaned_data.get('seat_type_2')
#         seat_type_3 = cleaned_data.get('seat_type_3')
#         # seat_type_1_upper = cleaned_data.get('seat_type_1_upper')
#         # seat_type_2_upper = cleaned_data.get('seat_type_2_upper')
#         # seat_type_3_upper = cleaned_data.get('seat_type_3_upper')
#         # seat_type_1_lower = cleaned_data.get('seat_type_1_lower')
#         # seat_type_2_lower = cleaned_data.get('seat_type_2_lower')
#         # seat_type_3_lower = cleaned_data.get('seat_type_3_lower')
#         number_or_column = cleaned_data.get('number_or_column')

#         if seat_type_1 == number_or_column and seat_type_2 and seat_type_3 != '0':
#             raise forms.ValidationError(
#                 "If seat_type_1 is equal to number_or_column, seat_type_2 must be 0.")

#         if seat_type_2 == number_or_column and seat_type_1 and seat_type_3 != '0':
#             raise forms.ValidationError(
#                 "If seat_type_2 is equal to number_or_column, seat_type_1 must be 0.")

#         if seat_type_3 == number_or_column and seat_type_1 and seat_type_2 != '0':
#             raise forms.ValidationError(
#                 "If seat_type_3 is equal to number_or_column, seat_type_1 and seat_type_2 must be 0.")

#         # if seat_type_1_upper == number_or_column and seat_type_2_upper and seat_type_3_upper != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_1_upper is equal to number_or_column, seat_type_2_upper must be 0.")

#         # if seat_type_2_upper == number_or_column and seat_type_1_upper and seat_type_3_upper != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_2_upper is equal to number_or_column, seat_type_1_upper must be 0.")

#         # if seat_type_3_upper == number_or_column and seat_type_1_upper and seat_type_2_upper != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_3_upper is equal to number_or_column, seat_type_1_upper and seat_type_2_upper must be 0.")

#         # if seat_type_1_lower == number_or_column and seat_type_2_lower and seat_type_3_lower != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_1_lower is equal to number_or_column, seat_type_2_lower must be 0.")

#         # if seat_type_2_lower == number_or_column and seat_type_1_lower and seat_type_3_lower != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_2_lower is equal to number_or_column, seat_type_1_lower must be 0.")

#         # if seat_type_3_lower == number_or_column and seat_type_1_lower and seat_type_2_lower != '0':
#         #     raise forms.ValidationError(
#         #         "If seat_type_3_lower is equal to number_or_column, seat_type_1_lower and seat_type_2_lower must be 0.")

#         return cleaned_data


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'coach', 'seat_number', 'price', 'is_booked']
