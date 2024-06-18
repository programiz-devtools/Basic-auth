from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user_management.models import User 
from django.contrib.auth import authenticate

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
     
      
        email = request.headers.get('email')
        password = request.headers.get('password')

     
        if not email or not password:
            return None 
       
        try:
             user = authenticate(email=email, password=password)
             request.user = user
            
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (user, None)
