from django.shortcuts import render
from django.views import View
from .. import decorators
from django.http import HttpResponse
# Create your views here.

class ManagerView(View):
    
    @decorators.validateRequetContentType
    @decorators.validateFieldsPresence
    @decorators.checkIfEmailAlreadyPresent
    def signUp(self, request): 
        return HttpResponse("Ok")