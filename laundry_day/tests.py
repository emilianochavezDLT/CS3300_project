from django.test import TestCase, Client
from django.contrib.auth.models import User
from laundry_day.models import UserProfile, LaundryRequests
from django.contrib.auth.hashers import check_password



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

    def test_login(self):
        for user in self.users:
            # Login
            response = self.client.post('/login/', {'username': user["username"], 'password': user["password"]}, follow=True)
            

            # Check response status code
            self.assertEqual(response.status_code, 200)

            # Check if user is logged in
            user_obj = User.objects.get(username=user["username"])
            self.assertEqual(int(self.client.session['_auth_user_id']), user_obj.pk)

            # Logout after each test
            self.client.logout()

    

#class LaundryRequestTestCase(TestCase):
#    def setUp(self):
#        self.user1 = User.objects.create_user(username="user1", password="password1")
#        self.user2 = User.objects.create_user(username="user2", password="password2")
#        self.user_profile1 = UserProfile.objects.create(user=self.user1)
#        self.user_profile2 = UserProfile.objects.create(user=self.user2)
#        self.laundry_request1 = LaundryRequests.objects.create(to_user=self.user_profile1, from_user=self.user_profile2, message="message1")
#        self.laundry_request2 = LaundryRequests.objects.create(to_user=self.user_profile2, from_user=self.user_profile1, message="message2")
#
#    def test_laundry_request(self):
#        laundry_request1 = LaundryRequests.objects.get(message="message1")
#        laundry_request2 = LaundryRequests.objects.get(message="message2")
#        self.assertEqual(laundry_request1.message, "message1")
#        self.assertEqual(laundry_request2.message, "message2")
#        self.assertEqual(laundry_request1.to_user, self.user_profile1)
#        self.assertEqual(laundry_request2.to_user, self.user_profile2)
#        self.assertEqual(laundry_request1.from_user, self.user_profile2)
#        self.assertEqual(laundry_request2.from_user, self.user_profile1)
#        self.assertEqual(laundry_request1.to_user.user.username, "user1")
#        self.assertEqual(laundry_request2.to_user.user.username, "user2")
#        self.assertEqual(laundry_request1.from_user.user.username, "user2")
#        self.assertEqual(laundry_request2.from_user.user.username, "user1")
#        self.assertEqual(laundry_request1.to_user.user, self.user1)
#        self.assertEqual(laundry_request2.to_user.user, self.user2)
#        self.assertEqual(laundry_request1.from_user.user, self.user2)
#        self.assertEqual(laundry_request2.from_user.user, self.user1)
#        self.assertEqual(laundry_request1.to_user.user.userprofile, self.user_profile1)
#        self.assertEqual(laundry_request2.to_user.user.userprofile, self.user_profile2)
#        self.assertEqual(laundry_request1.from_user.user.userprofile, self.user_profile2)
#        self.assertEqual(laundry_request2.from_user.user.userprofile, self.user_profile1)
#        self.assertEqual(laundry_request1.to_user.user.userprofile.user, self.user1)
#        self.assertEqual(laundry_request2.to_user.user.userprofile.user, self.user2)




    

    
    
    
    
    

    



    