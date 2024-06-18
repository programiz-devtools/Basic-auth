from django.db import models
import random

from django.contrib.auth.models import AbstractUser, BaseUserManager




class User(AbstractUser):
    USER_CHOICES = ((0, "Admin"), (1, "Organisation"))
    REGISTER_CHOICE = (
        (0, "inactive"),
        (1, "active"),
    )
    STATUS_CHOICES = (
        (0, "blocked"),
        (1, "unblock"),
    )

    user_type = models.IntegerField(choices=USER_CHOICES, default=1)
    email = models.EmailField(unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10, null=True)
    is_register = models.IntegerField(choices=REGISTER_CHOICE, default=0)
    external_login_provider=models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True) 

   
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # Add other required fields for creating a user
    class Meta:
        db_table = "users"
    def __str__(self):
        return self.email

    def json_object(self):
        return {
            "name": self.username,
            "email": self.email,
        }
