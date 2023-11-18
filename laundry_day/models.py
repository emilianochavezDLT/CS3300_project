from django.db import models
from django.urls import reverse

# Create your models here.

# This is the user model
class UserProfile(models.Model):

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    
    # We had to define the table name this way because
    # we already have a user table in the database
    class Meta:
        db_table = 'User_Profile'
    
    # This is the url that we want to redirect to when we
    # click on the user's name
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.user.id)])

    # This is the parent of the current user
    # If the user has no parent, this is null
    # This is essentially a foreign key to the user table and 
    # we are using the related_name to define the relationship
    # between the parent and the children
    parent = models.ForeignKey('self', 
                               null=True, 
                               blank=True, 
                               related_name='children',
                               on_delete=models.SET_NULL)  
   
    def get_parent(self):
        return self.parent
   

    
    # This is the list of siblings of the current user
    def get_siblings(self):
        if self.parent:

            # We want to exclude the current user from the list of siblings
            return self.parent.children.exclude(id=self.id)
        else:
            # If there is no parent, there are no siblings
            return UserProfile.objects.none()
        
    

class LaundryRequests(models.Model):
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='from_user')
    message = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.message
    
    def get_absolute_url(self):
        return reverse('create_laundry_request', args=[str(self.id)])
    
    


    
        
    
    
    
    

    