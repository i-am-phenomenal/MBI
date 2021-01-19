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
from ..Serializers.subscription_serializer import SubscriptionSerializer, SubscriptionCreateSerializer, SubscriptionListAPISerializer
from .mixin import ModelMixin, PermissionMixin


# class SubscriptionView(View): 

#     @decorators.validateRequestContentType
#     @decorators.validateHttpMethod
#     @decorators.validateIfAuthTokenPresent
#     @decorators.checkIfTokenExists
#     @decorators.validateFieldsForSubscription
#     @decorators.checkIfCustomerExists
#     @decorators.checkIfPriceExists
#     def createSubscription(self, customerId, priceId, paymentMethodId):
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         try: 
#             resp = stripe.Subscription.create(
#                 customer=customerId,
#                 items=[
#                     {"price": priceId},
#                 ]
#             )
#             print(resp)
#         except Exception as e: 
#             print(e)
#             return helpers.getBadResponse(str(e), 500)

#         Subscription.objects.create(
#             id= resp["id"],
#             customer = Manager.objects.get(id=customerId),
#             price_id = priceId,
#             insertedAt = datetime.now()
#         )
#         return HttpResponse(
#             json.dumps(
#                 {
#                     "message": "Create Sbscription successfully",
#                     "subscription": resp
#                 }
#             ),
#             content_type="application/json"
#         )

#     @decorators.validateIfAuthTokenPresentForGET
#     @decorators.checkIfTokenExistsForGET
#     def getAvailableSubscriptionsAndPrice(self, request, managerId): 
#         managerObject = Manager.objects.get(id=managerId)
#         allSubs = helpers.getAllSubscriptionsAndPrices(managerId)
#         return HttpResponse(
#             json.dumps(allSubs),
#             content_type="application/json"
#         )

#     @decorators.validateHttpMethod
#     @decorators.validateIfAuthTokenPresent
#     @decorators.checkIfTokenExists
#     def removeSubscription(self, request): 
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         params = helpers.getRequestParams(request)
#         try: 
#             resp = stripe.Subscription.delete(params["subscriptionId"])
#             print(resp)
#         except Exception as e: 
#             print(e)
#             return HttpResponse(str(e), 500)

#         subscriptionObject = Subscription.objects.get(id=params["subscriptionId"])
#         subscriptionObject.delete()
#         return HttpResponse(
#             json.dumps(
#                 {
#                     "message": "The user has been unsubscribed from the plan."
#                 }
#             ),
#             content_type="application/json"
#         )


class SubscriptionListCreateView(PermissionMixin, generics.ListCreateAPIView):
    """
    Generic API View for POST and GET all methods for Subscription

    Args:
        generics (Class): Generic API Class
    """ 
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionCreateSerializer

    def post(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        try: 
            resp = stripe.Subscription.create(
                customer=params["customerId"],
                items=[
                    {"price": params["priceId"]},
                ]
            )
            print(resp)
        except Exception as e: 
            print(e)
            return helpers.getBadResponse(str(e), 500)

        Subscription.objects.create(
            id= resp["id"],
            customer = Manager.objects.get(id=params["customerId"]),
            price_id = params["priceId"],
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

class SubscriptionRetreiveDestroyView(ModelMixin, PermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    Generic API View for GET and DELETE methods for Subscription
    Args:
        generics (Class): Generic API Class from Django Rest Framework
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def delete(self, request, id): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try: 
            resp = stripe.Subscription.delete(id)
            print(resp)
        except Exception as e: 
            print(e)
            return HttpResponse(str(e), 500)

        subscriptionObject = Subscription.objects.get(id=id)
        subscriptionObject.delete()
        return HttpResponse(
            json.dumps(
                {
                    "message": "The user has been unsubscribed from the plan."
                }
            ),
            content_type="application/json"
        )

class SubscriptionListAPIView(PermissionMixin, generics.ListAPIView):
    """
    Generic API View for List API for Subscriptions belonging to a customer
    Args:
        generics (Class): Generic API Class from Django Rest Framework
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionListAPISerializer
    lookup_field = "customer_id"