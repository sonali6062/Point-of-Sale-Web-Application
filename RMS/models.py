from django.db import models
from registrations.models import RestaurantRegistrationTable
# Create your models here.


class InventoryTable(models.Model):
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Ingredient_Name = models.CharField(max_length = 50);
    Inventory_Quantity = models.FloatField()
    Ingredient_Price = models.FloatField()
    Ingredient_PricePerGram = models.FloatField()

class MenuItemsTable(models.Model):
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Item_Name = models.CharField(max_length = 100)
    Item_Category = models.CharField(max_length = 20)
    Item_Type = models.CharField(max_length = 10)
    Cost_Price = models.FloatField()
    Item_GST = models.IntegerField()
    Item_ProfitMargin = models.IntegerField()
    Selling_Price = models.FloatField()
    Recipe = models.BooleanField(default=False)

class RecipeRequirementsTable(models.Model):
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Item = models.ForeignKey('MenuItemsTable', on_delete=models.CASCADE)
    Ingredient= models.ForeignKey('InventoryTable', on_delete=models.CASCADE)
    Ingredient_Name = models.CharField(max_length = 50);
    Ingredient_Quantity = models.FloatField()
    Ingredient_PricePerGram = models.FloatField()
    Total_Ingredient_Price = models.FloatField()

class SeatManagementTable(models.Model):
    Restaurant = models.ForeignKey(RestaurantRegistrationTable, on_delete=models.CASCADE)
    Table_Number = models.IntegerField()
    Number_Of_Covers = models.IntegerField()

