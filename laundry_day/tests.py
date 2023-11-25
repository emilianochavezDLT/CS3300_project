from django.test import TestCase, Client
from django.contrib.auth.models import User
from laundry_day.models import UserProfile, LaundryRequests
from django.contrib.auth.hashers import check_password
from .forms import *



class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = (
            {"first_name": "Frank", "last_name": "Doe", "username": "user1", "password": "testdata10"},
            {"first_name": "Jane", "last_name": "Foster", "username": "user2", "password": "testdata20"},
            {"first_name": "John", "last_name": "Foster", "username": "user3", "password": "testdata30"},
            {"first_name": "Jake", "last_name": "Doe", "username": "user4", "password": "testdata40"},
        )
        for user in self.users:
            User.objects.create_user(**user)

    


    

    
    
    
    
    

    



    