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
                    "message": "Created Price successfully."
                }
            ),
            content_type="application/json"
        )

    @decorators.checkIfGETMethod
    def getAllPrices(self, request):
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
        return HttpResponse(
            json.dumps(formatted),
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
        

