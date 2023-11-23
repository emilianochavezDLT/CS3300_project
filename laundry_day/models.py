from django.db import models
from django.urls import reverse

# Create your models here.

# This is the user model
class UserProfile(models.Model):

    # The user model is linked to the auth.User model
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    # The family field is a many to many field 
    # Which means that user can be in multiple families
    families = models.ManyToManyField("Family", blank=True)


    # We had to define the table name this way because
    # we already have a user table in the database
    class Meta:
        db_table = 'User_Profile'
    
    
    # This is the url that we want to redirect to when we
    # click on the user's name
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.user.id)])
   



class LaundryRequests(models.Model):
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='from_user')
    message = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.message
    
    class Meta:
        db_table = 'Laundry_Requests'
    
    def get_absolute_url(self):
        return reverse('create_laundry_request', args=[str(self.id)])
    
    
class Family(models.Model):

    # This is the family name
    family_name = models.CharField(max_length=100)

    # The family is given a code to uniquely identify the family
    family_code = models.CharField(max_length=4, null=True, default=None)

    # This is the family members, which is a many to many field 
    # Which means that user can be in multiple families. 
    # This relatioship is defined in the UserProfile model, but it not directly related 
    # The userprofile model is linked to the auth.User model
    # So when we access it we have to do it like this: user.family_members.all()
    family_members = models.ManyToManyField("auth.User", related_name='family_members')

    # This is for an example of how to get all families for a user

    # Get user with id 3
    #user = User.objects.get(id=3)

    # Get all families for this user
    #families = user.family_members.all()

    # Print all family names for this user
    #for family in families:
        #print(family.family_name)

    # Assuming you have a Family instance 'family'
    # for user in family.family_members.all():
        #print(user.username)

    def __str__(self):
        return self.family_name # This is what we want to show when we print the object
    
    class Meta: # This is the table name
        db_table = 'Family'

    # With this get_absolute_url method, we can now use the redirect function
    # to redirect to the family page after creating a new family object
    def get_absolute_url(self):
        return reverse('family_page', args=[str(self.id)]) 



    
        
    
    
    
    

    