from django.db import models

class User_Registration(models.Model):
    MoveEasePerson_choice = [(True,True),(False,False)]
    delivery_person_choice = [(True,True),(False,False)]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    MoveEasePerson = models.BooleanField(choices=MoveEasePerson_choice,default=False)
    delivery_person = models.BooleanField(choices=delivery_person_choice,default=False)
    contact = models.BigIntegerField()

class Booking_detail(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE)
    email =  models.EmailField()
    shifting_from = models.CharField(max_length=100)
    shifting_to = models.CharField(max_length=100) 
    bhk_type = models.CharField(max_length=10)
    service_time = models.DateTimeField()
    extra_cortans = models.CharField(max_length=10)
    selected_vehicle = models.CharField(max_length=50)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deliver_status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    delivery_person = models.CharField(max_length=100,default="None")
    
class customers_review(models.Model):
    name = models.CharField(max_length=20)
    rating = models.IntegerField()
    comments = models.TextField(max_length=200)