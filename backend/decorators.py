from . import helpers
from .models import *
from django.contrib.auth.hashers import check_password

def validateRequestContentType(function):
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

def validatePassword(function):
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        password = params["password"]
        validatePasswordLength = lambda password: len(password) >= 8
        validateIfUpperCaseLetterPresent = lambda password: any(character.isupper() for character in password)
        validateIfSpecialCharacterPresent = lambda password: any(character in "'!@#$%^&*()-+?_=,<>/'" for character in password)
        successCondition = (validatePasswordLength(password) and validateIfUpperCaseLetterPresent(password) and validateIfSpecialCharacterPresent(password))
        response = function(self, request) if successCondition else helpers.getBadResponse("Password must contain atleast 8 characters and one upper case letter and one special character", 400)
        return response
    return innerFunction

def validateFieldsForLogin(function): 
    def innerFunction(self, request):
        params = helpers.getRequestParams(request)
        successCondition = "emailId" in params and "password" in params
        resp = function(self, request) if successCondition else helpers.getBadResponse("Bad request. One or more important fields are missing", 400)
        return resp
    return innerFunction

def checkIfEmailPresent(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        getUserByEmailId = lambda emailId: Manager.objects.filter(emailId=emailId).exists()
        resp = function(self, request) if getUserByEmailId(params["emailId"]) else helpers.getBadResponse("User with the given email id does not exist", 400)
        return resp
    return innerFunction

def validateHttpMethod(function): 
    def innerFunction(self, request): 
        resp = function(self, request) if request.method == "POST" else helpers.getBadResponse("Bad request. Invalid HTTP request method", 400)
        return resp
    return innerFunction

def checkIfValidCreds(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        getManager = lambda emailId: Manager.objects.get(emailId=emailId)
        successCondition = check_password(params["password"], getManager(params["emailId"]).password)
        resp = function(self, request) if successCondition else helpers.getBadResponse("Invalid Credentials.", 400)
        return resp
    return innerFunction

def validateIfProductNamePresent(function):
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        resp = function(self, request) if "name" in params else helpers.getBadResponse("Bad request. Product name not present", 400)
        return resp
    return innerFunction

def validateIfProductNameAlreadyPresent(function):
    def innerFunction(self, request):
        params = helpers.getRequestParams(request)
        getProductByName = lambda name: Product.objects.filter(productName=name).exists()
        resp = function(self, request) if not getProductByName(params["name"]) else helpers.getBadResponse("Product with the given name already exists", 400)
        return resp
    return innerFunction


def validateMandatoryFieldsForPrice(function):
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        successCondition = "productId" in params and "currency" in params and "unitAmount" in params
        resp = function(self, request) if successCondition else helpers.getBadResponse("Bad request. One or more fields are missing", 400)
        return resp
    return innerFunction

def checkIfProductIdExists(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        getProductById = lambda id: Product.objects.filter(id=id).exists()
        resp = function(self, request) if not getProductById(params["productId"]) else helpers.getBadResponse("Product with the Id does not exist", 400)
        return resp
    return innerFunction

def checkIfGETMethod(function):
    def innerFunction(self, request):
        return function(self, request) if request.method == "GET" else helpers.getBadResponse("Invalid request method", 400)
    return innerFunction