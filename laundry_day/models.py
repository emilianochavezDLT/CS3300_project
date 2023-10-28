from django.db import models
from django.urls import reverse

# Create your models here.

# This is the user model
class User(models.Model):

    # We just want to define the name of the user
    # This just temporarily defines the user
    name = models.CharField(max_length=100)

    # This is the string representation of the user
    # This is what we want to display when we print the user
    def __str__(self):
        return self.name
    
    # We had to define the table name this way because
    # we already have a user table in the database
    class Meta:
        db_table = 'custom_user'
    
    # This is the url that we want to redirect to when we
    # click on the user's name
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

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

    
    # This is the list of siblings of the current user
    def get_siblings(self):
        if self.parent:

            # We want to exclude the current user from the list of siblings
            return self.parent.children.exclude(id=self.id)
        else:

            # If there is no parent, there are no siblings
            return User.objects.none()
        
    


    
    


    
        
    
    
    
    

    