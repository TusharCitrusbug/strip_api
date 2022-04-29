from pickle import FALSE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.]

class Plan(models.Model):
    Name=models.CharField(unique=True,max_length=100)
    plan_id=models.CharField(max_length=255,unique=True)
    Description=models.TextField()
    Price= models.FloatField(max_length=10000,null=False,blank=False) #cents
    Image=models.FileField(upload_to="images/", blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    isDelete = models.BooleanField(default = False)
    def __str__(self):
        return self.Name

class Customer(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255,unique=True)
    stripe_subscription_id = models.CharField(max_length=255,null=True,blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,null=True,blank=True)
    payment_method = models.CharField(max_length=200)
    wallet_balance=models.PositiveBigIntegerField(null=True,blank=True)
    buy_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=True)
    has_active_plan = models.BooleanField(default=False)

    def __str__(self):
        return self.stripe_id

# class Coupon(models.Model):
#     name = models.CharField(max_length=255)
#     discount_amount_in_percentage = models.IntegerField()

#     def __str__(self):
#         return self.name