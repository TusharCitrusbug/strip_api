from pickle import FALSE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.]
CHOICES =(
    ("1", "card"),
    ("2", "online"),
)
class Product(models.Model):
    Name=models.CharField(unique=True,max_length=100)
    Description=models.TextField()
    Price= models.FloatField(max_length=10000,null=False,blank=False) #cents
    Image=models.FileField(upload_to="images/", blank=True, null=True)
    def __str__(self):
        return self.Name

class Customer(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=200,choices=CHOICES)
    wallet_balance=models.PositiveBigIntegerField()
    def __str__(self):
        return self.email
