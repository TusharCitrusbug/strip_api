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

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

class GoogleLoginSerializer(serializers.Serializer):

    pass

class FacebookLoginSerializer(serializers.Serializer):

    pass





