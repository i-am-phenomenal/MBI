from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime
from rest_framework import generics
from ..Serializers.product_serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated

class ProductView(View): 

    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateIfProductNamePresent
    @decorators.validateIfProductNameAlreadyPresent
    def createProduct(self, request): 
        params = helpers.getRequestParams(request)
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        try: 
            resp = stripe.Product.create(
                name= params["name"]
            )
            Product.objects.create(
                id = resp["id"],
                productName = resp["name"],
                insertedAt = datetime.now()
            )
        except Exception as e: 
            print(e)
        return HttpResponse("Ok")


class ProductListCreateView(generics.ListCreateAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        print(serializer)
        return HttpResponse("Ok")