from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics,status
from .models import User
from .serializers import SignupSerializer,LoginSerializer,UserSerializer,UserDataSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from basic.authentication import CustomAuthentication
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate,login
from .permission import IsCustomAuthenticated,IsSessionAuthenticated,IsJWTAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .permission import IsSessionAuthenticated,IsSessionAuthenticated2
from django.contrib.sessions.backends.db import SessionStore

def handle_validation_error(e):
    response={}
   
    try:
        error_message = str(e).split("ErrorDetail(string='")[1].split("'")[0]
        return Response(
                {"message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            ) 
    except Exception as e:
        return Response(
            
           {"message":"Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
 
        )

class SignUpView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            print(serializer.validated_data)
            user1 = User.objects.get(username=serializer.data['username'])
            return Response(serializer.data,status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return handle_validation_error(e)
        
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes=[]
    permission_classes=[]

    def create(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
      
        serializer =  self.get_serializer(data=request.data)
        try:

       
            serializer.is_valid(raise_exception = True)
            user = serializer.validated_data["user"]
            username=user.username
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            session = SessionStore()
            session['username'] = username
            session.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            access["user_type"]=user.user_type
            access_token=str(access)

            return Response({"access_token":access_token})
        
        except serializers.ValidationError as e:
            return handle_validation_error(e)

class UserListView(generics.ListAPIView):
  
    authentication_classes=[SessionAuthentication]
    permission_classes = [IsSessionAuthenticated2] 
    serializer_class = UserSerializer

    def get_queryset(self):
      
        user_type = self.request.query_params.get('user_type', None)
        if user_type is not None:
            return User.objects.filter(user_type=user_type)
        return []
    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer =self.get_serializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDataSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes = [IsSessionAuthenticated2]

    def get(self, request, *args, **kwargs):
        user_id=kwargs.get('id')
        try:

         user=User.objects.get(id=user_id)
         serializer = self.get_serializer(user)
         return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
    
    

     




       
           
          
        
        
        
        
       