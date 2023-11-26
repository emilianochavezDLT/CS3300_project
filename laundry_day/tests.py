from django.test import TestCase, Client
from django.contrib.auth.models import User
from laundry_day.models import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .forms import *
from django.urls import reverse
from django.core.exceptions import ValidationError


class UserProfileCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1qdfds3') # Create a user
        
    def test_user_profile_creation(self):
        self.assertTrue(isinstance(self.user.userprofile, UserProfile)) # Check that the userprofile is created
        self.assertEqual(self.user.userprofile.user, self.user) # Check that the userprofile is linked to the user
        
        
    def test_user_profile_exists(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists()) # Check that the userprofile exists


class AddingFamilyMembers(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1qdfds3') # Create a user
        self.user2 = User.objects.create_user(username='testuser2', password='1qdfds3') 
        self.user3 = User.objects.create_user(username='testuser3', password='1qdfds3') 
        self.family = Family.objects.create(family_name='testfamily', family_code='1234') 
        self.family.family_members.add(self.user) # Add the user to the family because the user is the creator of the family
        self.family.save() # Save the family
    
    # This test is to check that the form is valid and that the user is added to the family
    # A user can only add one user at a time to the family.
    # The user can only add a user to the family if the username and family code is correct
    def test_valid_form(self):
        form = AddFamilyMembersForm({'username': 'testuser2', 'family_code': '1234'}) # Create a form with the username and family code
        self.assertTrue(form.is_valid()) # Check that the form is valid
        username = form.cleaned_data.get('username') # Get the username from the form
        user = User.objects.get(username=username) # Get the user object from the username
        self.family.family_members.add(user) # Add the user to the family
        self.assertEqual(self.family.family_members.count(), 2) # 2 because we added the user in the setup
        self.assertEqual(self.family.family_name, 'testfamily') # Check that the family name is correct
        self.assertEqual(self.family.family_members.all()[0].username, 'testuser') # Check that the first user is correct
        self.assertEqual(self.family.family_members.all()[1].username, 'testuser2') # Check that the second user is correct
    

    def test_invalid_username(self):
        form = AddFamilyMembersForm({'username': 'wronguser', 'family_code': '1234'}) # Create a form with the username and family code
        self.assertFalse(form.is_valid()) # Check that the form is invalid
        self.assertEqual(form.errors['username'], ['Username might be incorrect']) # Check that the error message is correct

    def test_invalid_family_code(self):
        form = AddFamilyMembersForm({'username': 'testuser', 'family_code': '1527'}) # Create a form with the username and family code
        self.assertFalse(form.is_valid()) # Check that the form is invalid
        self.assertEqual(form.errors['family_code'], ['Family code might be incorrect']) # Check that the error message is correct

    def test_missing_username(self):
        form = AddFamilyMembersForm({'family_code': '1234'}) # Create a form with the username and family code
        self.assertFalse(form.is_valid()) # Check that the form is invalid
        self.assertEqual(form.errors['username'], ['This field is required.']) # Check that the error message is correct

    def test_missing_family_code(self):
        form = AddFamilyMembersForm({'username': 'testuser'}) # Create a form with the username and family code
        self.assertFalse(form.is_valid()) # Check that the form is invalid
        self.assertEqual(form.errors['family_code'], ['This field is required.']) # Check that the error message is correct


    
class TestLaundryRequest(TestCase):
        
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1qdfds3')
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user2 = User.objects.create_user(username='testuser2', first_name='Test', last_name='User2', password='1qdfds3')
        self.user_profile2 = UserProfile.objects.get(user=self.user2)
        self.family = Family.objects.create(family_name='testfamily', family_code='1234')
        self.family.family_members.add(self.user, self.user2)
        self.family.save()
    
    def test_valid_form(self):
        form = CreateLaundryRequest(user=self.user, data={'to_user': self.user_profile2, 'message': 'test message'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('to_user'), self.user_profile2)
        self.assertEqual(form.cleaned_data.get('message'), 'test message')
        
        laundry_request = form.save(commit=False)
        laundry_request.from_user = self.user_profile
        laundry_request.save()
        saved_laundry_request = LaundryRequests.objects.get(to_user=self.user_profile2, from_user=self.user_profile, message='test message')
        self.assertEqual(LaundryRequests.objects.count(), 1)
        self.assertEqual(saved_laundry_request.to_user, self.user_profile2)
        self.assertEqual(saved_laundry_request.from_user, self.user_profile)
        self.assertEqual(saved_laundry_request.message, 'test message')
        
    def test_invalid_form(self):
        form = CreateLaundryRequest(user=self.user, data={'to_user': self.user_profile2, 'message': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'], ['This field is required.'])
    
    def update_laundry_request(self):
        form = UpdateLaundryRequest(user=self.user, data={'to_user': self.user_profile2, 'message': 'New test message'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('to_user'), self.user_profile2)
        self.assertEqual(form.cleaned_data.get('message'), 'New test message')

        laundry_request = form.save(commit=False)
        laundry_request.from_user = self.user_profile
        laundry_request.save()
        saved_laundry_request = LaundryRequests.objects.get(to_user=self.user_profile2, from_user=self.user_profile, message='New test message')
        self.assertEqual(LaundryRequests.objects.count(), 1)
        self.assertEqual(saved_laundry_request.to_user, self.user_profile2)
        self.assertEqual(saved_laundry_request.from_user, self.user_profile)
        self.assertEqual(saved_laundry_request.message, 'New test message')
        

        
        

        
        


        
         