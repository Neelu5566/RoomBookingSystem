from django.db import models
from django.contrib.auth.models import User

# # Create your models here.
# class Resource(models.Model):
#     ROOM_CATEGORIES=(
#         ('VCR',"Video Conference Room"),
#         ('MR',"Meeting Room"),
#         ('240S',"240 Seater"),
#         ('120-A',"120 Seater Room-1"),
#         ('120-B',"120 Seater Room-2"),
#         ('PMR',"Personal Meeting Room")
        
        
#     )
#     number = models.IntegerField()
#     category = models.CharField(max_length=5,choices=ROOM_CATEGORIES)
#     capacity=models.IntegerField()
#     seats=models.IntegerField()

#     def __str__(self):
#         return f'{self.number}.  {self.category} with {self.seats} for {self.category} people'

# class user_detail(models.Model):
    
#     username=models.CharField(max_length=100,null=True)
#     email=models.EmailField(primary_key=True)
#     password = models.CharField(max_length=50)
#     confirm_password = models.CharField(max_length=50)
#     mobile_number =models.CharField(max_length=14)

#     def __str__(self):
#         return self.username

#     def save(self, *args, **kwargs):
#         super(user_detail, self).save(*args, **kwargs)

# class Booking_detail(models.Model):
#     TIME=(
#         ("1hr","1 Hour"),
#         ("2hr","2 Hour"),
#         ("3hr","3 Hour"),
#         ("4hr+","4 Hour +"),
        
#     )
#     TIME_PARITY=(
#         ("AM","AM"),
#         ("PM","PM"),
        
#     )
#     id=models.AutoField(primary_key=True)
#     fullname=models.CharField(max_length=100,null=True)
#     date=models.DateField()
#     slot = models.CharField(max_length=5,choices=TIME)
#     start= models.TimeField()
#     start_parity=models.CharField(max_length=2,choices=TIME_PARITY)
#     end= models.TimeField()
#     end_parity=models.CharField(max_length=2,choices=TIME_PARITY)
#     description=models.TextField()
#     def __str__(self):
#         return str(self.id) +". " +self.fullname

class Room_details(models.Model):
    roomName = models.CharField(max_length=200)
    roomDescription = models.TextField()
    def __str__(self):
            return self.roomName

class Booking_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room_details, on_delete=models.CASCADE)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    description = models.TextField()
    def __str__(self):
        return self.user.username + " " + self.room.roomName + " " + str(self.date) + " " + str(self.startTime) + " " + str(self.endTime) 


    

