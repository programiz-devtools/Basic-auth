# myapp/permissions.py
from rest_framework.permissions import BasePermission
from basic.authentication import CustomAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

class IsCustomAuthenticated(BasePermission):
    """
    Allows access only to users authenticated via CustomAuthentication.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and isinstance(request.successful_authenticator, CustomAuthentication)

class IsSessionAuthenticated2(BasePermission):
    """
    Allows access only to users authenticated via session authentication.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and isinstance(request.successful_authenticator, SessionAuthentication)
      
    
class IsSessionAuthenticated(BasePermission):
    def has_permission(self, request, view):
        import pdb;pdb.set_trace()
        # Retrieve session key from request headers or any other source
        session_key = request.headers.get('Session-Key')
        if session_key:
            try:
                # Retrieve session data using the session key
                session = Session.objects.get(session_key=session_key)
                # Retrieve username from session data
                username = session.get_decoded().get('username')
                # Check if username exists in session data
                return username is not None
            except Session.DoesNotExist:
                return False
        return False

class IsJWTAuthenticated(BasePermission):
    """
    Allows access only to users authenticated via JWT authentication.
    """
    def has_permission(self, request, view):
        import pdb;pdb.set_trace()
        return (
            request.user and 
            request.user.is_authenticated and 
            isinstance(request.successful_authenticator, JWTAuthentication)
        )
