from rest_framework import serializers 
from ..models import Product

class ProductSerializer(serializers.ModelSerializer): 
    productName = serializers.CharField(max_length=50)
    
    class Meta: 
        model = Product
        fields = [
            "productName"
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