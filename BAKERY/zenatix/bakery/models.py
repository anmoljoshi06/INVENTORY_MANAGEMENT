from django.db import models
from django.conf import settings
# Create your models here.
from django.core.validators import MaxValueValidator

class ingredients(models.Model):
    item = models.CharField(max_length=100,unique=True)         #name of the ingredient
    total_quantity = models.IntegerField(null=True,blank=True)  #Qunatity in numbers
    unit = models.CharField(max_length=15,blank=True)           #Scalar unit for the measurement (e.g Kg,Ltr,Lbs)
    quantity_added = models.IntegerField(null=True,blank=True)  #quantity added (if required)
    added_date = models.DateTimeField(auto_now=True)            #Datetime on which new quantity was added
    price_per_unit = models.IntegerField(null=True,blank=True)  #Price per unit of each item

class Bakery_Item_Names(models.Model):
    bakery_item = models.CharField(max_length=100,unique=True)
    cost_price = models.IntegerField()
    added_date = models.DateTimeField(auto_now=True) 
    price = models.IntegerField()                                #seling price
    discount = models.IntegerField(default=0,blank=True,validators=[MaxValueValidator(100)])         #Taken as a percentage by default 

class Bakery_item_recipe(models.Model):
    bakery_item =  models.ForeignKey(Bakery_Item_Names, on_delete=models.CASCADE)
    item = models.ForeignKey(ingredients, on_delete=models.CASCADE)
    percentage = models.IntegerField(null=True,blank=True)


class orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bakery_item = models.ForeignKey(Bakery_Item_Names, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    order_time = models.TimeField(auto_now=True)
    quantity = models.IntegerField(null=True,blank=True)                 # note add class Meta here to filter the orders by date
    cost = models.IntegerField(null=True,blank=True)


