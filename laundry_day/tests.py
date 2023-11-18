from django.test import TestCase
from django.contrib.auth.models import User
from laundry_day.models import UserProfile, LaundryRequests
from django.contrib.auth.hashers import check_password


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_user_profile(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        self.assertEqual(user1.username, "user1")
        self.assertEqual(user2.username, "user2")
        self.assertTrue(check_password("password1", user1.password))
        self.assertTrue(check_password("password2", user2.password))

    def test_user_profile(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        user_profile1 = UserProfile.objects.create(user=user1)
        user_profile2 = UserProfile.objects.create(user=user2)
        self.assertEqual(user_profile1.user.username, "user1")
        self.assertEqual(user_profile2.user.username, "user2")
        self.assertEqual(user_profile1.user, user1)
        self.assertEqual(user_profile2.user, user2)
        

class LaundryRequestTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.user_profile1 = UserProfile.objects.create(user=self.user1)
        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.laundry_request1 = LaundryRequests.objects.create(to_user=self.user_profile1, from_user=self.user_profile2, message="message1")
        self.laundry_request2 = LaundryRequests.objects.create(to_user=self.user_profile2, from_user=self.user_profile1, message="message2")

    def test_laundry_request(self):
        laundry_request1 = LaundryRequests.objects.get(message="message1")
        laundry_request2 = LaundryRequests.objects.get(message="message2")
        self.assertEqual(laundry_request1.message, "message1")
        self.assertEqual(laundry_request2.message, "message2")
        self.assertEqual(laundry_request1.to_user, self.user_profile1)
        self.assertEqual(laundry_request2.to_user, self.user_profile2)
        self.assertEqual(laundry_request1.from_user, self.user_profile2)
        self.assertEqual(laundry_request2.from_user, self.user_profile1)
        self.assertEqual(laundry_request1.to_user.user.username, "user1")
        self.assertEqual(laundry_request2.to_user.user.username, "user2")
        self.assertEqual(laundry_request1.from_user.user.username, "user2")
        self.assertEqual(laundry_request2.from_user.user.username, "user1")
        self.assertEqual(laundry_request1.to_user.user, self.user1)
        self.assertEqual(laundry_request2.to_user.user, self.user2)
        self.assertEqual(laundry_request1.from_user.user, self.user2)
        self.assertEqual(laundry_request2.from_user.user, self.user1)
        self.assertEqual(laundry_request1.to_user.user.userprofile, self.user_profile1)
        self.assertEqual(laundry_request2.to_user.user.userprofile, self.user_profile2)
        self.assertEqual(laundry_request1.from_user.user.userprofile, self.user_profile2)
        self.assertEqual(laundry_request2.from_user.user.userprofile, self.user_profile1)
        self.assertEqual(laundry_request1.to_user.user.userprofile.user, self.user1)
        self.assertEqual(laundry_request2.to_user.user.userprofile.user, self.user2)




    

    
    
    
    
    

    



    