from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime

class PriceView(View):

    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateMandatoryFieldsForPrice
    @decorators.checkIfProductIdExists
    def createPrice(self, request): 
        params = helpers.getRequestParams(request)
        stripe.api_key = settings.STRIPE_SECRET_KEY 
        try:
            resp =  stripe.Price.create(
                unit_amount=params["unitAmount"],
                currency=params["currency"],
                recurring = {
                    "interval": "month" 
                },
                product= params["productId"]
            )
        except Exception as e: 
            print(e)
        return HttpResponse("Ok")

    @decorators.checkIfGETMethod
    def getAllPrices(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        prices = stripe.Price.list(limit=10)
        print(prices)
        return HttpResponse('Ok')
