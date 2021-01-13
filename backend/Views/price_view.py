from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime
import json

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
        return HttpResponse(
            json.dumps(
                {
                    "message": "Created Price successfully."
                }
            ),
            content_type="application/json"
        )

    @decorators.checkIfGETMethod
    def getAllPrices(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        prices = stripe.Price.list(limit=10)
        print(prices)
        return HttpResponse(
            json.dumps(prices),
            content_type="application/json"
        )

    @decorators.checkIfDELETEMethod
    @decorators.checkIfProductIdPresent
    def deletePriceById(self, request, priceId): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        priceExists = lambda priceId: Price.objects.filter(id=priceId).exists()
        try: 
            stripe.Price.delete(priceId)
        except Exception as e: 
            print(e)
        response = HttpResponse("Deleted Price.", content_type="application/json")
        if not priceExists(priceId):
            return response

        else: 
            Price.objects.get(id=priceId).delete()
            return response
        

