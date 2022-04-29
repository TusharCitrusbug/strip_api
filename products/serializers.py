from rest_framework import serializers
from  products.models import *

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
       model=Plan
       fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
       model=Customer
       fields='__all__'

    