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