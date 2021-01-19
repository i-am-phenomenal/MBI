from django.shortcuts import render
from django.views import View
from .. import decorators
from django.http import HttpResponse
from ..models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .. import helpers
import json
from ..authentication_utils import AuthenticationUtils
from rest_framework.authtoken.models import Token 
import stripe
from django.conf import settings
from rest_framework import generics
from ..Serializers.manager_serializer import ManagerSerializer, ManagerGetPaymentMethodSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .mixin import ModelMixin, PermissionMixin

# Create your views here.

class ManagerView(View):
    
    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateFieldsPresence
    @decorators.checkIfEmailAlreadyPresent
    @decorators.validatePassword
    def signUp(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        try: 
            resp = stripe.Customer.create(
                email = params["emailId"],
                name = params["firstName"] + " " + params["lastName"]
            )
            print(resp)
        except Exception as e: 
            print(e)
        managerObject = Manager(
            id = resp["id"],
            emailId = params["emailId"],
            password = make_password(params["password"]),
            company = params["company"],
            dateOfBirth = helpers.convertStrtoDate(params["dateOfBirth"]),
            firstName = "" if "firstName" not in params else params["firstName"],
            lastName = "" if "lastName" not in params else params["lastName"],
            insertedAt = datetime.now()
        )
        managerObject.save()
        
        converted = vars(managerObject)
        return HttpResponse(
            json.dumps(
                helpers.getManagetDict(converted, "User Created Successfully")
            ),
            content_type="application/json",
            status=200
        )

    def login(self, request): 
        params = helpers.getRequestParams(request)
        authenticationUtils = AuthenticationUtils()
        managerObject = Manager.objects.get(emailId = params["emailId"])
        token, _ = Token.objects.get_or_create(user=managerObject)
        if authenticationUtils.checkIfTokenExpired(token): 
                token = authenticationUtils.renewToken(token)
        responseDict = {
            "userDetails": helpers.getManagetDict(vars(managerObject), "User Logged In"),
            "authToken": token.key
        }
        return HttpResponse(
            json.dumps(
                responseDict
            ),
            content_type="application/json",
            status=200
        )

    @decorators.checkIfGETMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    def getManagerDetailsByToken(self, request):
        token = helpers.getTokenFromRequest(request) 
        authenticationUtils = AuthenticationUtils()
        managerObject = authenticationUtils.getUserByToken(token)
        return HttpResponse(
            json.dumps(
                helpers.getManagetDict(vars(managerObject), "Ok")
            ),
            content_type="application/json"
        )

class ManagerListCreateView(generics.ListCreateAPIView):
    """
    Generic API View for POST and GET all methods for Manager

    Args:
        generics (Class): Generic API Class
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [AllowAny]

class ManagerRetreiveDestroyView(ModelMixin, generics.RetrieveUpdateDestroyAPIView): 
    """
    Generic API View for GET and DELETE methods for Manager
    Args:
        DealerMixin (Class): Mixin Class to set the lookup field to id 
        generics (Class): Generic API Class
    """
    permission_classes = [AllowAny]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class ManagerUpdateView(PermissionMixin, generics.UpdateAPIView): 
    """
    Generic API View for Update methods for Manager
    Args:
        DealerMixin (Class): Mixin Class to set the lookup field to id 
        generics (Class): Generic API Class
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def put(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)

        try:
            resp = stripe.PaymentMethod.attach(
                params["paymentMethodId"],
                customer=params["managerId"],
            )
            stripe.Customer.modify(
                params["managerId"],
                invoice_settings=
                {
                    "default_payment_method": params["paymentMethodId"]
                },
            )
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("There was an error in adding card details. Please try again later.", 500)
        
        managerObject = Manager.objects.get(id=params["managerId"])
        paymentMethodObject = PaymentMethod.objects.get(id=params["paymentMethodId"])
        managerObject.cardDetails = paymentMethodObject
        managerObject.save()

        return HttpResponse(
            json.dumps(
                {
                    "Message": "Updated card details successfully",
                    "manager": resp
                }
            ),
            content_type="application/json"
        )

class ManagerRetreivePaymentMethod(ModelMixin, PermissionMixin, generics.RetrieveAPIView): 
    """
    View class for GET for Manager's payment method

    Args:
        generics (Class): Generic API Class
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerGetPaymentMethodSerializer

class ManagerRemoveCardDetailsView(PermissionMixin, generics.DestroyAPIView):
    """
    View class for DELETE for Manager's payment method

    Args:
        generics (Class): Generic API Class
    """
    queryset = Manager.objects.all()

    def delete(self, request, paymentMethodId): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try: 
            resp = stripe.PaymentMethod.detach(
                paymentMethodId
            )
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("")

        paymentMethod = PaymentMethod.objects.get(id=paymentMethodId).delete()
        return HttpResponse(
            json.dumps(
                {
                    "message": "Removed Card Details Successfully",
                    "details": resp
                }
            ),
            content_type="application/json"
        )