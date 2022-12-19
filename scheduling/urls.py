from django.urls import path
from .views import *


urlpatterns = [
    path("",homePage,name="home"),
    path("signup/",register,name="register"),
    path("login/",loginUser,name="login"),
    path("logout/",logoutUser,name="logout"),
    path("date_booking/Booking/<str:roomName>/<str:date>",booking_details,name="Booking_Details"),
    path("get_slots/<str:roomName>",get_slots,name="get_slots"),
    path("date_booking/<str:roomName>",date_filter,name="date_booking"),
    path("notify/<str:roomName>/<str:date>/<str:startTime>/<str:endTime>",notify_mail,name="notify_mail"),
    path("delete_slot/<str:roomName>/<str:date>/<str:startTime>/<str:endTime>",delete_slot,name="delete_slot"),
    

]  
