from . import helpers
from .models import Manager

def validateRequetContentType(function):
    def innerFunction(self, request):
        successCondition = request.content_type == "application/json"
        response = function(self, request) if successCondition else helpers.getBadResponse("Bad Request. Invalid Content Type", 400)
        return response
    return innerFunction

def validateFieldsPresence(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        successCondition = "emailId" in params and "password" in params and "company" in params and "dateOfBirth" in params
        response = function(self, request) if successCondition else helpers.getBadResponse("Bad request. One or more fields are missing", 400)
        return response
    return innerFunction

def checkIfEmailAlreadyPresent(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        getUserByEmail = lambda emailId: Manager.objects.filter(emailId=emailId).exists()
        response = function(self, request) if not getUserByEmail(params["emailId"]) else helpers.getBadResponse("User with emailId already exists", 400)
        return response
    return innerFunction