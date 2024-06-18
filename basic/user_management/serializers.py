from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate

 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']


class SignupSerializer(serializers.Serializer):
    USER_CHOICES =( 
    ("1", "Manager"), 
    ("2", "Staff"), 
    ("3", "Customer"), 
   
) 


    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
  

    def validate(self, data):
        import pdb;pdb.set_trace()
        password = data['password']
        confirm_password = data['confirm_password']
        username = data['username']
        email = data['email']
       

        if email == None:
            raise serializers.ValidationError("Email is required")

        if password != confirm_password:
            raise serializers.ValidationError('Password does not match')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already in use')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already in use')

        return data

    def create(self, validated_data):
     
     validated_data.pop('confirm_password')
     user = User.objects.create(
         username=validated_data['username'],
         email=validated_data['email'],
        
    )
     user.set_password(validated_data['password'])
     user.save()
     


    
     return user

     

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        import pdb;pdb.set_trace()
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Unable to log in with the provided credentials.')
        else:
            raise serializers.ValidationError('Must include username" and password')

        return data
