from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#We are going to create new user form
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name','last_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
 
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2






#This is to create a laundry request
class CreateLaundryRequest(forms.ModelForm):
    class Meta:
        model = LaundryRequests
        fields = '__all__'

    


    
    
    
        

        

    
    

    
    
    
    
    
    
    