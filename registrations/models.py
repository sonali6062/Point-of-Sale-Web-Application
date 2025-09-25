from django.contrib.auth.models import AbstractUser
from django.db import models 

# Create your models here.
class User(AbstractUser):
    is_restAdmin = models.BooleanField(default = False)
    is_restManager = models.BooleanField(default=False)
    is_restStaff = models.BooleanField(default=False)
    contact=models.BigIntegerField()
    address=models.TextField()

class RestaurantRegistrationTable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    Restaurant_name=models.CharField(max_length=100)
    Restaurant_address=models.TextField()
    Admin_AccessID = models.CharField(max_length=20)
  
class ManagerRegistrationTable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Admin_AccessID = models.CharField(max_length=20)
    Manager_Salary=models.FloatField()
    Manager_AccessID = models.CharField(max_length=20)

class StaffRegistrationTable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Manager_AccessID = models.CharField(max_length=20)
    Staff_designation = models.CharField(max_length=50)
    Staff_Salary=models.FloatField()
