from rest_framework import serializers 
from ..models import Subscription
from .manager_serializer import ManagerSerializer
from .price_serializer import PriceSerializer


class SubscriptionCreateSerializer(serializers.ModelSerializer): 
    customerId = serializers.CharField(max_length=50)
    priceId = serializers.CharField(max_length=50)
    paymentMethodId = serializers.CharField(max_length=50)

class SubscriptionSerializer(serializers.ModelSerializer): 
    customer = ManagerSerializer(many=False)
    price = PriceSerializer(many=False)

    class Meta: 
        model = Subscription
        fields = [
            "customer",
            "price",
            "insertedAt",
            "updatedAt"
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

class SubscriptionListAPISerializer(serializers.ModelSerializer): 
    id = serializers.CharField(max_length=20)
    price = PriceSerializer(many=False)

    class Meta: 
        model = Subscription
        fields = [
            "id",
            "price",
        ]

class ManagerSubscriptionSerializer(serializers.ModelSerializer): 
    customer_id = serializers.CharField(max_length=20)
    price = PriceSerializer(many=False)

    class Meta: 
        model = Subscription
        fields = [
            "customer_id",
            "price"
        ]