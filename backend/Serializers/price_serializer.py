from rest_framework import serializers 
from ..models import Price
from .product_serializer import ProductSerializer

class PriceSerializer(serializers.ModelSerializer): 
    currency = serializers.CharField(max_length=10)
    unitAmount = serializers.IntegerField()
    billingScheme = serializers.CharField(max_length=20)
    interval = serializers.CharField(max_length=10)
    intervalCount = serializers.IntegerField()
    product  = ProductSerializer(many=False)

    class Meta: 
        model = Price
        fields = [
            "currency",
            "unitAmount",
            "billingScheme", 
            "interval",
            "intervalCount",
            "insertedAt",
            "updatedAt",
            "product",
        ]
        extra_kwargs = {
            "insertedAt": {
                'read_only': True,
                'required': False
            },
            "updatedAt": {
                'read_only': True,
                'required': False
            },
        }
