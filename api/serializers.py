from django.db.models import fields
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    # amount = serializers.DecimalField(
    #     max_digits=10, decimal_places=2, min_value=0,
    #     error_messages={
    #         'min_value': 'Amount value should be greater than or equal to 0.',
    #         'invalid': 'Please enter a valid amount.'
    #     }
    # )
    
    class Meta:
        model = Item
        fields = ('category', 'subcategory', 'name', 'amount')