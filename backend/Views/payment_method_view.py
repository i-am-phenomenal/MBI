from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime
import json

class PaymentMethodView(View): 

    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    @decorators.validateFieldsForPayment
    @decorators.checkIfCardAlreadyExists
    @decorators.checkIfCardExpired
    @decorators.validatePaymentParams
    def createPaymentMethod(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        try: 
            resp = stripe.PaymentMethod.create(
                type="card",
                card={
                    "number": params["cardNumber"],
                    "exp_month": params["expiryMonth"],
                    "exp_year": params["expiryYear"],
                    "cvc": params["cvv"],
                }
            )
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("There was an error while creating Payment. Please try again later", 500)
        
        PaymentMethod.objects.create(
            id = resp["id"],
            cardNumber = params["cardNumber"],
            expiryMonth = params["expiryMonth"],
            expiryYear = params["expiryYear"],
            cvv = params["cvv"],
            insertedAt = datetime.now()
        )
        return HttpResponse(
            json.dumps(
                {
                    "Message": "Payment method created successfully",
                    "Details" : resp
                }
            ),
            content_type = "application/json"
        )