from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from datetime import date 
import datetime

today = date.today()
today= today.strftime("%d/%m/%Y")
time = datetime.datetime.now()
time = time.strftime("%H:%M:%S")



# Create your views here.
@login_required(login_url='login')
def homePage(request):
    user_rooms = Booking_details.objects.filter(user=request.user)
    rooms = Room_details.objects.all()
    user = request.user
    # print(rooms)
    return render(request,"home.html",{'rooms':rooms,'user_rooms':user_rooms,'user':user})

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'login.html')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html', {'form': form})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='login')
def booking_details(request,roomName,date):
    room = Room_details.objects.get(roomName=roomName)
    slots = Booking_details.objects.filter(date=date,room=room)
    prevdate = date
    if request.method == "POST":
        user = request.user
        date=request.POST['date']
        stime=request.POST['stime']
        sparity=request.POST['sparity']
        etime=request.POST['etime']
        eparity=request.POST['eparity']
        description=request.POST['description']
        if date!=prevdate:
            messages.success(request,"Date should be same as selected")
            return redirect(booking_details,roomName,date)
        if date < today:
            messages.success(request,"Date should be greater than today")
            return redirect(booking_details,roomName,date)
        
        if stime > etime:
            messages.success(request,"Start time should be less than end time")
            return redirect(booking_details,roomName,date)
        if stime < time and date == today:
            messages.success(request,"Start time should be greater than current time")
            return redirect(booking_details,roomName,date)

        already_existed = Booking_details.objects.filter(date=date,room=room,startTime=stime,endTime=etime)
        if already_existed:
            messages.success(request,"Slot already booked")
            return redirect(booking_details,roomName,date)
        Book= Booking_details(room = room,user=user,date=date,startTime=stime,endTime=etime,description=description)

        Book.save()
        msg = f"Dear {user.username} \n Your Booking for {roomName} is confirmed on {date} from {stime} to {etime}" 
        sub = "Slot Conformation mail"
        send_mail(sub,msg,settings.EMAIL_HOST_USER,[user.email],fail_silently=False)

        messages.success(request,"Booking succesfully")
        return redirect(homePage)
    else:
        return render(request,"booking details.html",{'slots':slots,'roomName':roomName})

    #     try:
    #    
    
            
    #         Book.save()
    #         messages.success(request,"Booking succesfully")
    #         return redirect(homePage)
    #     except:
    #         messages.success(request,"something happend try again after sometime")

    
    # return render(request,"scheduling/booking details.html")
@login_required(login_url='login')
@csrf_exempt
def get_slots(request,roomName):
    if request.method == "POST":
        date = request.POST['date']
        # print(date)
        slots = Booking_details.objects.filter(date=date,room_name=roomName)
        # print(slots)
        return render(request,"booking details.html",{'slots':slots})
    else:
        return render(request,"booking details.html")
@login_required(login_url='login')
def date_filter(request,roomName):
    if request.method == "POST":
        date = request.POST['date']
        # print(date)
        # room = Room_details.objects.get(roomName=roomName)
        # slots = Booking_details.objects.filter(date=date,room=room)
        # print(slots)
        return redirect(f'Booking/{roomName}/{date}')
        # return render(request,"booking details.html",{'slots':slots})
    else:
        return render(request,"date booking.html",{'roomName':roomName})
@login_required(login_url='login')
def notify_mail(request,roomName,date,startTime,endTime):
    user = request.user
    room = Room_details.objects.get(roomName=roomName)
    booked_slot = Booking_details.objects.get(date=date,startTime=startTime,endTime=endTime,room=room)

    notify = notify_details(notify_mail = user.email,booked_slot=booked_slot)
    notify.save()
    messages.success(request,"You will be notified for that slot")
    return redirect(homePage)
@login_required(login_url='login')
def delete_slot(request,roomName,date,startTime,endTime):
    user = request.user
    room = Room_details.objects.get(roomName=roomName)
    booked_slot = Booking_details.objects.get(date=date,startTime=startTime,endTime=endTime,room=room,user=user)
    mail_persons = notify_details.objects.filter(booked_slot=booked_slot)
    msg = f"Your request slot for {roomName} is free from {startTime} to {endTime} on {date}" 
    sub = "Slot free"
    for mail_person in mail_persons:
        to = [mail_person.notify_mail]
        # print(to)
        send_mail(sub,msg,settings.EMAIL_HOST_USER,to,fail_silently=False)
    booked_slot.delete()
    messages.success(request,"Slot deleted")
    return redirect(homePage)




