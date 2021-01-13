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


    @decorators.validateRequestContentType
    @decorators.validateHttpMethod
    @decorators.validateFieldsForLogin
    @decorators.checkIfEmailPresent
    @decorators.checkIfValidCreds
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

    def addPaymentMethod(self, request): 
        pass

    @decorators.validateRequestContentType
    @decorators.validateIfPUTMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    @decorators.validateFieldsForCardDetails
    @decorators.checkIfManagerExists
    @decorators.checkIfCardDetailsExists
    def updatePaymentMethod(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)

        try: 
            resp = stripe.PaymentMethod.attach(
                params["paymentMethodId"],
                customer=params["managerId"],
            )
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("There was an error in adding card details. Please try again later.", 500)
        
        managerObject = Manager.objects.get(id=params["managerId"])
        managerObject.cardDetails = PaymentMethod.objects.get(id=params["paymentMethodId"])
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

    @decorators.validateRequestContentType
    @decorators.checkIfDELETEMethod
    @decorators.validateIfAuthTokenPresent
    @decorators.checkIfTokenExists
    @decorators.checkIfPaymentIdPresent
    @decorators.checkIfPaymentMethodExists
    def removePaymentMethod(self, request): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        params = helpers.getRequestParams(request)
        try: 
            resp = stripe.PaymentMethod.detach(
                params["paymentMethodId"]
            )
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("")

        paymentMethod = PaymentMethod.objects.get(id=params["paymentMethodId"]).delete()
        return HttpResponse(
            json.dumps(
                {
                    "message": "Removed Card Details Successfully",
                    "details": resp
                }
            ),
            content_type="application/json"
        )

    # @decorators.validateRequestContentType
    # @decorators.checkIfGETMethod
    # @decorators.validateIfAuthTokenPresent
    # @decorators.checkIfTokenExists
    # @decorator.checkIfManagerIdPresent
    # @decorators.checkIfManagerExists
    def getAllPaymentMethods(self, request, managerId): 
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try: 
            resp = stripe.PaymentMethod.list(
                customer=managerId,
                type="card",
            )
            print(resp)
        except Exception as e: 
            print(e)
            return helpers.getBadResponse("There was an error while getting payment methods. Please try again later", 500)

        return HttpResponse(
            json.dumps(resp),
            content_type="application/json"
        )
        