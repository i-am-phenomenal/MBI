from rest_framework import serializers 
from ..models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer): 
    type = serializers.CharField(max_length=50)
    cardNumber = serializers.CharField(max_length=50)
    expiryMonth = serializers.IntegerField()
    expiryYear = serializers.IntegerField()
    cvv = serializers.CharField(max_length=3)

    class Meta:
        model = PaymentMethod
        fields = [
            "type",
            "cardNumber",
            "expiryMonth", 
            "expiryYear",
            "cvv",
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
