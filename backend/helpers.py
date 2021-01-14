from django.http import HttpResponse
import json
from datetime import datetime

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
        "message": message
    }

def getTokenFromRequest(request):
    headers = request.headers
    authToken = headers["Authorization"].split(" ")[1]
    return authToken