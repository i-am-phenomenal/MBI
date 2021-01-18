from django.contrib.auth.models import BaseUserManager

class MyManager(BaseUserManager): 
    def get_by_natural_key(self, id): 
        manager = self.get(id=id)
        return manager