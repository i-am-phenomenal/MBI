from django.contrib.auth.models import BaseUserManager

class MyManager(BaseUserManager): 
    def get_by_natural_key(self, emailId):
        print(emailId, "222222222222222222222") 
        manager = self.get(emailId=emailId)
        print(manager.firstName, "333333333333333333333333")
        return manage