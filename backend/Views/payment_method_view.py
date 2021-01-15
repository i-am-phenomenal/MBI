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
                    "number": params["cardNumber"].strip(),
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

    @decorators.validateIfAuthTokenPresentForGET
    @decorators.checkIfTokenExistsForGET
    def getCardDetails(self, request, managerId):
        manager = Manager.objects.get(id=managerId)
        cardDetails = manager.cardDetails
        if cardDetails is None: 
            return HttpResponse(
                json.dumps(""),
                content_type="application/json"
            )
        return HttpResponse(
            json.dumps(
                {
                    "type": cardDetails.type, 
                    "cardNumber": cardDetails.cardNumber, 
                    "expiryMonth": cardDetails.expiryMonth,
                    "expiryYear": cardDetails.expiryYear,
                    "cvv": cardDetails.cvv
                }
            ),
            content_type="application/json"
        ) 

    def setupPaymentIntent(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        try: 
            resp = stripe.SetupIntent.create(
                payment_method_types=["card"],
                customer=params["customerId"],
                payment_method=params["paymentMethodId"]
            )
            print(resp)
        except Exception as e: 
            print(e)
            return helpers.getBadResponse(str(e), 500)

        return HttpResponse("Setup Payment Intent Successful !")

    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    @decorators.validateFieldsForPaymentIntent
    @decorators.validateIfRecordsExist
    @decorators.checkIfSubscriptionExist
    def createPaymentIntent(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        subscription = Subscription.objects.get(id=params["subscriptionId"])
        priceObject = Price.objects.get(id=subscription.price_id)
        try: 
            resp = stripe.PaymentIntent.create(
                amount=priceObject.unitAmount,
                currency=priceObject.currency,
                payment_method_types=["card"],
                customer=params["customerId"],
                payment_method=params["paymentMethodId"]
            )
            print(resp)
        except Exception as e: 
            print(e)
            return helpers.getBadResponse(str(e), 500)
        return HttpResponse(
            json.dumps(resp),
            content_type="application/json"
        )
        
