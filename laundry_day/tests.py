from django.test import TestCase
from laundry_day.models import User

# Create your tests here.
class ShowNameTest(TestCase):

    #This is the setup method for getting a user
    def setUp(self):
        user = User.objects.get(id=3)
        self.assertEqual(str(user.name), 'Alan Doe')




    