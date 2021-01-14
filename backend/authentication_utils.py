from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token 

class AuthenticationUtils(): 
    """
        Class to provide Utility functions for authentication purposes. 
        Primarilty checks/generates authentication tokens to be sent to the client
    """

    def isExpired(self, tokenObject): 
        """
        Checks if token expired or not.
        Performs the check on the basis of time difference between when the token was expired and till current time
        being called from 'checkIfTokenExpired' of the current class
        
        Args:
            tokenObject (Class Token): [Object of class Token]

        Returns:
            timeLeft [timeDelta]: [time difference the time when tokenObject was created and till now]
        """
        timeElapsed = timezone.now() - tokenObject.created
        timeLeft = timedelta(seconds = settings.TOKEN_LIFETIME) - timeElapsed
        return timeLeft

    def checkIfTokenExpired(self, tokenObject): 
        """
        Checks if token expired or not.
        Performs the check on the basis of time difference between when the token was expired and till current time

        Args:
            tokenObject (Class Token): [Object of class Token]

        Returns:
            [True/False]: [Boolean]
        """
        return self.isExpired(tokenObject) < timedelta(seconds=0)

    def renewToken(self, tokenObject): 
        """
        Function to renew an expired token.

        Args:
            tokenObject (Class Token): [Object of class Token]

        Returns:
            tokenObject (Class Token): [Object of class Token]
        """
        tempUser = tokenObject.user
        tokenObject.delete()
        newToken = Token.objects.create(user=tempUser)
        return newToken

    def tokenExists(self, token): 
        return True if Token.objects.filter(key=token).exists() else False

    def getUserByToken(self, tokenKey):
        tokenObject = Token.objects.get(key=tokenKey)
        return tokenObject.user

    