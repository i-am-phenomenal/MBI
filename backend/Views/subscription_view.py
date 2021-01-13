from django.views import View
from django.http import HttpResponse
from django.conf import settings
import stripe
from .. import decorators
from .. import helpers
from ..models import *
from datetime import datetime


class SubscriptionView(View): 

    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    @decorators.validateFieldsForSubscription
    @decorators.checkIfCustomerExists
    @decorators.checkIfPriceExists
    def createSubscription(self, customerId, priceId): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try: 
            resp = stripe.Subscription.create(
                customer=customerId,
                items=[
                    {"price": priceId},
                ],
            )
            print(resp)
        except Exception as e: 
            print(e, "1111111111111111111111111111")

        Subscription.objects.create(
            id= resp["id"],
            customer = Manager.objects.get(id=customerId),
            price = Price.objects.get(id=priceId),
            insertedAt = datetime.now()
        )
        return HttpResponse(
            json.dumps(
                {
                    "message": "Create Sbscription successfully",
                    "subscription": resp
                }
            ),
            content_type="application/json"
        )
