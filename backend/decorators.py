from . import helpers
from .models import *
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token 
from .authentication_utils import AuthenticationUtils
from datetime import datetime

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

def validateIfPUTMethod(fn): 
    def innerFn(self, request): 
        return fn(self, request) if request.method == "PUT" else helpers.getBadResponse("Bad Request. Invalid HTTP Method", 400)
    return innerFn

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
        resp = function(self, request) if getProductById(params["productId"]) else helpers.getBadResponse("Product with the Id does not exist", 400)
        return resp
    return innerFunction

def checkIfGETMethod(function):
    def innerFunction(self, request):
        return function(self, request) if request.method == "GET" else helpers.getBadResponse("Invalid request method", 400)
    return innerFunction

def checkIfDELETEMethod(function): 
    def innerFunction(self, request): 
        return function(self, request) if request.method == "DELETE" else helpers.getBadResponse("Invalid request method.", 400)
    return innerFunction 

def checkIfProductIdPresent(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        return function(self, request, params["priceId"]) if "priceId" in params else helpers.getBadResponse("Price Id not present in request", 400)
    return innerFunction

def validateIfAuthTokenPresent(function): 
    def innerFunction(self, request):
        headers = request.headers
        successCondition = ("Authorization" in headers) or ("authorization") in headers
        response = function(self, request) if successCondition else helpers.getBadResponse("Malformed request. Authorization header not present in the request", 401)
        return response
    return innerFunction

def validateIfAuthTokenPresentForGET(fn): 
    def innerFn(self, request, managerId): 
        headers = request.headers
        successCondition = ("Authorization" in headers) or ("authorization") in headers
        response = fn(self, request, managerId) if successCondition else getBadResponse("Malformed request. Authorization header not present in the request", 401)
        return response
    return innerFn

def checkIfTokenExists(function):
    def innerFunction(self, request):
        authUtils = AuthenticationUtils()
        headers = request.headers
        authToken = headers["Authorization"].split(" ")[1]
        return function(self, request) if authUtils.tokenExists(authToken) else helpers.getBadResponse("Token does not exist", 401)
    return innerFunction

def checkIfTokenExistsForGET(fn):
    def innerFn(self, request, managerId): 
        authUtils = AuthenticationUtils()
        headers = request.headers
        authToken = headers["Authorization"].split(" ")[1]
        return fn(self, request, managerId) if authUtils.tokenExists(authToken) else helpers.getBadResponse("Token does not exist", 401)
    return innerFn

def checkIfTokenExpired(function): 
    def innerFunction(self, request): 
        authUtils = AuthenticationUtils()
        headers = request.headers
        authToken = headers["Authorization"].split(" ")[1]
        getToken = lambda key: Token.objects.get(key=key)
        return function(self, request) if not authUtils.checkIfTokenExpired(getToken(authToken)) else helpers.getBadResponse("Invalid Auth Token. Please Login once again", 401)
    return innerFunction

def validateFieldsForSubscription(function):
    def innerFunction(self, request):
        params = helpers.getRequestParams(request)
        successCondition = "customerId" in params and "priceId" in params and "paymentMethodId" in params
        return function(self, params["customerId"], params["priceId"], params["paymentMethodId"]) if successCondition else helpers.getBadResponse("One or more fields missing", 400)
    return innerFunction

def checkIfCustomerExists(function): 
    def innerFunction(self, customerId, priceId, paymentMethodId): 
        managerExists = lambda id: Manager.objects.filter(id=id).exists()
        return function(self, customerId, priceId, paymentMethodId) if managerExists(customerId) else helpers.getBadResponse("Customer does not exist", 400)
    return innerFunction

def checkIfPriceExists(function): 
    def innerFunction(self, customerId, priceId, paymentMethodId): 
        priceExists = lambda id: Price.objects.filter(id=id).exists()
        return function(self, customerId, priceId, paymentMethodId) if priceExists(priceId) else helpers.getBadResponse("Price does not exist", 400)
    return innerFunction

def validateFieldsForPayment(function): 
    def innerFunction(self, request): 
        params = helpers.getRequestParams(request)
        cond = "cardNumber" in params and "expiryMonth" in params and "expiryYear" in params and "cvv" in params
        return function(self, request) if cond else helpers.getBadResponse("Bad request. One or more fields are missing", 400)
    return innerFunction

def checkIfCardAlreadyExists(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        getCard = lambda cardNumber: PaymentMethod.objects.filter(cardNumber=cardNumber).exists()
        return fn(self, request) if not getCard(params["cardNumber"]) else helpers.getBadResponse("Card with the given number already exists", 500)
    return innerFn

def checkIfCardExpired(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        today = datetime.today().date()
        successCond = today < datetime(year = params["expiryYear"], month=params["expiryMonth"], day=1).date()
        return fn(self, request) if successCond else helpers.getBadResponse("Card is Expired. Please enter a new card", 500)
    return innerFn

def validatePaymentParams(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        successCond = len(params["cardNumber"]) == 16 and len(params["cvv"]) == 3
        return fn(self, request) if successCond else helpers.getBadResponse("Invalid card number or cvv. Please try again", 500)
    return innerFn

def validateFieldsForCardDetails(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        return fn(self, request) if ("paymentMethodId" in params and "managerId" in params) else helpers.getBadResponse("Invalid Request Body", 400)
    return innerFn

def checkIfManagerExists(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        managerExists = lambda id: Manager.objects.filter(id=id).exists()
        return fn(self, request) if managerExists(params["managerId"]) else helpers.getBadResponse("Manager with the given id does not exist", 500)
    return innerFn

def checkIfCardDetailsExists(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        cardDetailsExists = lambda id: PaymentMethod.objects.filter(id=id).exists()
        return fn(self, request) if cardDetailsExists(params["paymentMethodId"]) else helpers.getBadResponse("Invalid Card details", 400)
    return innerFn

def checkIfPaymentMethodExists(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        paymentMethodExists = lambda id: PaymentMethod.objects.filter(id=id).exists()
        return fn(self, request) if paymentMethodExists(params["paymentMethodId"]) else helpers.getBadResponse("Payment method does not exist", 400)
    return innerFn

def checkIfPaymentIdPresent(fn): 
    def innerFn(self, request): 
        params = helpers.getRequestParams(request)
        return fn(self, request) if "paymentMethodId" in params else helpers.getBadResponse("Payment Method Id not present", 400)
    return innerFn

def validateFieldsForPaymentMethod(fn): 
    def innerFn(self, request):
        params = helpers.getRequestParams(request)
        successCondition = "paymentMethodId" in params and "managerId" in params
        return fn(self, request) if successCondition else helpers.getBadResponse("One or more fields are missing.", 400)
    return innerFn