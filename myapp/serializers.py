from rest_framework import serializers
from .models import Account, Destination

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    HTTP_METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        # Add more choices as needed
    ]
    
    # Use ChoiceField for http_method with predefined choices
    http_method = serializers.ChoiceField(choices=HTTP_METHOD_CHOICES)

    class Meta:
        model = Destination
        fields = ['id', 'account', 'url', 'http_method', 'headers']
