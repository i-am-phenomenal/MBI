from django.shortcuts import render
from django.views import View
from .. import decorators
from django.http import HttpResponse
from ..models import Manager
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