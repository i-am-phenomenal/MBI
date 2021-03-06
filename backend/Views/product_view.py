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
from .mixin import ModelMixin, PermissionMixin

class ProductListCreateView(PermissionMixin, generics.ListCreateAPIView):
    """
    Generic API View for POST and GET all methods for Product

    Args:
        generics (Class): Generic API Class
    """ 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request): 
        params = helpers.getRequestParams(request)
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        try: 
            resp = stripe.Product.create(
                name= params["productName"]
            )
        except Exception as e: 
            print("EXCEPTION -> ", e)
        Product.objects.create(
            id = resp["id"],
            productName = resp["name"],
            insertedAt = datetime.now()
        )
        return HttpResponse(json.dumps(resp), content_type="application/json")

class ProductRetreiveDestroyView(ModelMixin, PermissionMixin, generics.RetrieveUpdateDestroyAPIView): 
    """
    Generic API View for GET and DELETE methods for Product
    Args:
        generics (Class): Generic API Class from Django Rest Framework
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer