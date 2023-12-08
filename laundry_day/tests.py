from django.test import TestCase, Client
from django.contrib.auth.models import User
from laundry_day.models import *
from .forms import *
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
from selenium.webdriver.common.by import By



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

class MySeleniumTests(LiveServerTestCase):
    def setUp(self):
        options = Options()
        
        #For git actions
        options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #self.driver = webdriver.Chrome(options=options)
        
        
        #This is to run the tests locally with the chrome driver
        options.headless = False
        self.driver = webdriver.Chrome(service=Service('/Users/Echav/Documents/CS3300/Projects/CS3300_project/chromedriver'), options=options)

         # Check if the server is running
        response = requests.get(self.live_server_url)
        if response.status_code != 200:
            raise Exception('Server is not running')
        
        self.user = User.objects.create_user(username='testuser', password='1qdfds3E', first_name='test', last_name='user') # Create a user

    def tearDown(self):
        self.driver.quit()

    #def test_title(self):
    #    self.driver.get(self.live_server_url)
    #    time.sleep(5)
    #    assert 'Laundry Day' in self.driver.title, 'Title is not correct'

    #The user should be able to login
    # We are using the testuser that we created in the setup
    # First name is test, last name is user
    #The username is testuser and the password is 1qdfds3E
    def test_login(self):
        self.driver.get(self.live_server_url)
        time.sleep(5)
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(5)
        self.driver.find_element(By.ID, 'id_username').send_keys('testuser')
        self.driver.find_element(By.ID, 'id_password').send_keys('1qdfds3E')
        time.sleep(5)
        self.driver.find_element(By.ID, 'login_button').click()
        time.sleep(5)
        assert 'Laundry Day' in self.driver.title, 'Title is not correct'
        assert 'test' in self.driver.page_source, 'First_name is not correct'
        assert 'user' in self.driver.page_source, 'Last_name is not correct'
        assert 'Login' not in self.driver.page_source, 'Login button is present'

    #The user should be able to logout
    # We are using the testuser that we created in the setup
    # First name is test, last name is user
    #The username is testuser and the password is 1qdfds3E

    def test_logout(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'id_username').send_keys('testuser')
        self.driver.find_element(By.ID, 'id_password').send_keys('1qdfds3E')
        self.driver.find_element(By.ID, 'login_button').click()
        assert 'Logout' in self.driver.page_source, 'Logout button is not present'
        self.driver.find_element(By.ID, 'logout_button').click()
        time.sleep(5)
        assert 'Login' in self.driver.page_source, 'Login button is not present'
        assert 'Username' in self.driver.page_source, 'Username not is present'
        assert 'Password' in self.driver.page_source, 'Password is not present'

    #The user should be able to create a family
    # We are using the testuser that we created in the setup
    # First name is test, last name is user
    #The username is testuser and the password is 1qdfds3E
    #The family name is testfamily and the family code is 1234
    def test_create_family(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element(By.ID, 'login_button').click()
        self.driver.find_element(By.ID, 'id_username').send_keys('testuser')
        self.driver.find_element(By.ID, 'id_password').send_keys('1qdfds3E')
        self.driver.find_element(By.ID, 'login_button').click()
        
        #You have to specify the full path to the chromedriver
        #If you have a clickable elements amoung other elements, 
        #then you have to specify the full path to the element
        self.driver.find_element(By.ID, 'Family_dropdown').click() # Click on the family dropdown
        self.driver.find_element(By.ID, 'create_family_navbar').click() # Then click on the create family button
        time.sleep(5)
        self.driver.find_element(By.ID, 'family_name').send_keys('testfamily')
        self.driver.find_element(By.ID, 'family_code').send_keys('1234')
        self.driver.find_element(By.ID, 'create_family_button').click()
        time.sleep(5)
        assert 'testfamily' in self.driver.page_source, 'Family name is not present'
        assert '1234' not in self.driver.page_source, 'Family code is present'
        
        