from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime
import json
from rest_framework import generics
from ..Serializers.price_serializer import PriceSerializer
from rest_framework.permissions import IsAuthenticated
from .mixin import ModelMixin, PermissionMixin  

class PriceListCreateView(PermissionMixin, generics.ListCreateAPIView):
    """
    Generic API View for POST and GET all methods for Price

    Args:
        generics (Class): Generic API Class
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    def post(self, request): 
        params = helpers.getRequestParams(request)
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        try:
            resp =  stripe.Price.create(
                unit_amount=params["unitAmount"],
                currency=params["currency"],
                recurring = {
                    "interval": params["interval"]
                },
                product= params["productId"]
            )
        except Exception as e: 
            print(e)
        Price.objects.create(
            id = resp["id"],
            product = Product.objects.get(id=resp["product"]),
            currency = resp["currency"],
            unitAmount = resp["unit_amount"],
            intervalCount = resp["recurring"]["interval_count"],
            insertedAt = datetime.now()
        )
        return HttpResponse(
            json.dumps(
                {
                    "message": "Created Price successfully.",
                    "details": resp
                }
            ),
            content_type="application/json"
        )

    def get(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        prices = stripe.Price.list(limit=10)["data"]
        formatted = [
            {
                "priceId": price["id"],
                "currency": price["currency"],
                "interval": price["recurring"]["interval"],
                "intervalCount": price["recurring"]["interval_count"],
                "product": helpers.getFormattedProductDetails(stripe.Product.retrieve(price["product"])),
                "unitAmount": price["unit_amount"]
            }
            for price in prices
        ]
        helpers.populateProductIfDoesNotExist(formatted)
        helpers.populatePricesIfDoesNotExist(formatted)
        return HttpResponse(
            json.dumps(formatted),
            content_type="application/json"
        )

class PriceRetreiveDestroyView(ModelMixin, PermissionMixin, generics.RetrieveUpdateDestroyAPIView): 
    """
    Generic API View for GET and DELETE methods for Price
    Args:
        generics (Class): Generic API Class from Django Rest Framework
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    