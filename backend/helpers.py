from django.http import HttpResponse
import json
from datetime import datetime
from .models import *

def getBadResponse(message, statusCode): 
    return HttpResponse(
        json.dumps(
            {
                "message": message
            }
        ),
        status=statusCode,
        content_type="application/json"
    )

def getRequestParams(requestObject): 
    params = requestObject.body.decode("utf-8")
    params = json.loads(params)
    return params

def convertStrtoDate(dateStr): 
    formatted = datetime.strptime(dateStr, "%d/%m/%Y").date()
    return formatted

def convertDateToStr(date): 
    return str(date.day) + "/" + str(date.month) + "/" + str(date.year)

def getManagetDict(converted, message): 
    return {
        "id": str(converted["id"]),
        "emailId": converted["emailId"],
        "company" : converted["company"],
        "firstName": converted["firstName"],
        "lastName": converted["lastName"],
        "dateOfBirth": convertDateToStr(converted["dateOfBirth"]),
        "message": message,
        "paymentMethodId": converted["cardDetails_id"]
    }

def getTokenFromRequest(request):
    headers = request.headers
    authToken = headers["Authorization"].split(" ")[1]
    return authToken

def getAllSubscriptionsAndPrices(managerId):
    subs = Subscription.objects.filter(customer_id=managerId)
    if subs == [] or subs == None:
        return []
    else:
        formatted = [
            {
                "productName": sub.price.product.productName,
                "currency": sub.price.currency,
                "unitAmount": sub.price.unitAmount,
                "billingScheme": sub.price.billingScheme,
                "interval": sub.price.interval,
                "intervalCount": sub.price.intervalCount,
                "subscriptionId": sub.id
            }
            for sub in subs
        ]
        return formatted

def getFormattedProductDetails(fetched): 
    return {
        "name": fetched["name"],
        "productId": fetched["id"]
    }

def populateProductIfDoesNotExist(prices):
    productExists = lambda id: Product.objects.filter(id=id).exists()
    for element in prices:
        if not (productExists(element["product"])): 
            try:
                Product.objects.create(
                    id=element["product"]["productId"],
                    productName=element["product"]["name"],
                    insertedAt=datetime.now(),
                )
                print("Product Created !")
            except Exception as e:
                print(e)
                pass

def populatePricesIfDoesNotExist(prices):
    priceExists = lambda priceId: Price.objects.filter(id=priceId).exists() 
    for price in prices:
        if not (priceExists(price["priceId"])):
            try:
                Price.objects.create(
                    id=price["priceId"],
                    currency=price["currency"],
                    interval=price["interval"],
                    intervalCount=price["intervalCount"],
                    unitAmount=price["unitAmount"],
                    insertedAt=datetime.now(),
                    product_id=price["product"]["productId"]
                )
                print("Price Created !")
            except Exception as e:
                print(e)
                pass
