from django.shortcuts import render
from django.views import View
from .. import decorators
from rest_framework.decorators import api_view
from django.http import HttpResponse
from ..models import Manager
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .. import helpers
import json
# Create your views here.

class ManagerView(View):
    
    @decorators.validateRequestContentType
    # @api_view(["POST"])
    @decorators.validateFieldsPresence
    @decorators.checkIfEmailAlreadyPresent
    @decorators.validatePassword
    def signUp(self, request): 
        params = helpers.getRequestParams(request)
        managerObject = Manager(
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
                {
                    "uuid": str(converted["uuid"]),
                    "emailId": converted["emailId"],
                    "company" : converted["company"],
                    "firstName": converted["firstName"],
                    "lastName": converted["lastName"],
                    "message": "Created User Successfully",
                }
            ),
            content_type="application/json",
            status=200
        )