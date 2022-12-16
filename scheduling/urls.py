from django.urls import path
from .views import *


urlpatterns = [
    path("",homePage,name="home"),
    path("signup/",register,name="register"),
    path("login/",loginUser,name="login"),
    path("logout/",logoutUser,name="logout"),
    # path("Booking/",views.booking_details,name="Booking_Details"),
    

]  
