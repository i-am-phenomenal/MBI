from rest_framework import serializers 
from ..models import Manager


class ManagerSerializer(serializers.ModelSerializer): 
    emailId = serializers.CharField(max_length=50)
    firstName = serializers.CharField(max_length=50)
    lastName = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=200)
    company = serializers.CharField(max_length=50)

    class Meta: 
        model = Manager
        fields = [
            "firstName",
            "lastName",
            "emailId",
            "password",
            "company",
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
