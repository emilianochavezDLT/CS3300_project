from django.db import models
from django.urls import reverse

# Create your models here.
class User(models.Model):

    # We just want to define the name of the user
    # This just temporarily defines the user
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'custom_user'
        
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    parent = models.ForeignKey('self', 
                               null=True, 
                               blank=True, 
                               related_name='children',
                               on_delete=models.SET_NULL)    
    
    


    
        
    
    
    
    

    