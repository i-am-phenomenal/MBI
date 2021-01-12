from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime


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
                productId = resp["id"],
                productName = resp["name"],
                insertedAt = datetime.now()
            )
        except Exception as e: 
            print(e)
        return HttpResponse("Ok")