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



# Create your views here.
@login_required(login_url='login')
def homePage(request):
    rooms = Room_details.objects.all()
    print(rooms)
    return render(request,"home.html",{'rooms':rooms})

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

def logoutUser(request):
    logout(request)
    return redirect('login') 

def booking_details(request):
    # if request.method == "POST":
    #     name=request.POST['firstName']
    #     date=request.POST['date']
    #     slot=request.POST['slot']
    #     stime=request.POST['stime']
    #     sparity=request.POST['sparity']
    #     etime=request.POST['etime']
    #     eparity=request.POST['eparity']
    #     description=request.POST['description']

    #     try:
    #         Book=Booking_detail(fullname=name,date=date,slot=slot,start=stime,start_parity=sparity,end=etime,end_parity=eparity,description=description)
    #         #user_obj=User.objects.create_user(name=fname+" "+lname,gender=gender,dob=dob,height=height,weight=weight,email=email)
            
    #         Book.save()
    #         messages.success(request,"Booking succesfully")
    #         return redirect(homePage)
    #     except:
    #         messages.success(request,"something happend try again after sometime")

    
    # return render(request,"scheduling/booking details.html")
    return render(request,"booking details.html")
@csrf_exempt
def get_slots(request):
    if request.method == "POST":
        date = request.POST['date']
        print(date)
        slots = Booking_details.objects.filter(date=date)
        print(slots)
        return HttpResponse(slots, status=201)

