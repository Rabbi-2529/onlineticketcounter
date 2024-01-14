import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from bus.models import Staffs 


def staff_home(request):
   
    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    

    return render(request,"staff_template/staff_home_template.html",)
def ticket_booking(request):
    return render(request,'staff_template/ticketbooking.html')
