from rest_framework import serializers
from  products.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
       model=Product
       fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
       model=Customer
       fields='__all__'