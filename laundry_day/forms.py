from typing import Any
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#We are going to create new user form
class CreateUserForm(UserCreationForm):

    #This is the meta class
    class Meta:
        model = User #This is the model that we are going to use

        #These are the fields that we are going to use
        fields = ['first_name',
                  'last_name', 
                  'username', 
                  'password1', 
                  'password2'
                ]
        
    #This is the save method
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False) #This is the super class
        user.first_name = self.cleaned_data["first_name"] #This is the first name 
        user.last_name = self.cleaned_data["last_name"] #This is the last name
        user.username = self.cleaned_data["username"] # This is the username
        if commit:
            user.save() #This is to save the user
        return user #This is to return the user

    #This is the clean method for username
    def clean_username(self):
        username = self.cleaned_data['username'] #This is the username
        if User.objects.filter(username=username).exists(): #This is to check if the username exists
            raise forms.ValidationError("Username already exists") #This is to raise the error
        return username #This is to return the username
    
    #This is the clean method for password
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 != password2: #This is to check if the passwords match
            raise forms.ValidationError("Passwords do not match") #This is to raise the error
        return password2 #This is to return the password
    
    # This is the init method where I am adding the classes to the fields
    # So, that they can be styled
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['last_name'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['password1'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['password2'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100) #This is the username with max length of 100
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput) #This is the password with max length of 100 and it is a password input
    
    def clean_username(self):
        username = self.cleaned_data['username'] #This is the username making sure that it is cleaned
        if not User.objects.filter(username=username).exists(): #This is to check if the username exists
            raise forms.ValidationError("Username does not exist") #This is to raise the error
        return username #This is to return the username
    
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is None: #This is to check if the username is none
            raise forms.ValidationError("Username is required.") #This is to raise the error
        user = User.objects.filter(username=username).first() #This is to get the user
        if user is None: #This is to check if the user is none
            raise forms.ValidationError("Username does not exist.") #This is to raise the error
        if not user.check_password(password): #This is to check if the password is correct
            raise forms.ValidationError("Password is incorrect") #This is to raise the error
        return password #This is to return the password
    
    # Some more styling
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
                                                     'id':'id_username'
                                                     })
        self.fields['password'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6', 
                                                     'id':'id_password'
                                                     })

#This is to create a laundry request
class CreateLaundryRequest(forms.ModelForm):
    class Meta:
        model = LaundryRequests
        fields = ['to_user', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) # This is to get the user from the view and request
        super(CreateLaundryRequest, self).__init__(*args, **kwargs) # This is to call the super class
        if user: # This is to check if the user exists
            user_profile = UserProfile.objects.get(user=user) # This is to get the user profile, but i didn't use it
            print(f"User: {user.family_members.all()}") 
            families = user.family_members.all() # This is to get all the families for the user
            member_names = [] # This is to store the member names
            
            # To get the member names, I needed to do a for loop
            for family in families: # This is to loop through the families
                for member in family.family_members.all(): # This is to loop through the family members
                    member_names.append(member.first_name+" "+member.last_name) # This is to append the member names to the member_names list
                    if member == user: # This is to check if the logged in user is in the family
                        member_names.remove(member.first_name+" "+member.last_name) # if they are then remove them from the list to be selected

            print(member_names)
            
            # Here we are just extracting the first name and last name from the member names list
            # After doing this, we are going to use this to filter by first name and last name
            # This just helps to match the first name and last name of the owner of the user profile
            # This is a longer way of doing it, but it works. I'm pretty suer I could've done it by id
            queryset = UserProfile.objects.filter(user__first_name__in=[name.split()[0] for name in member_names], user__last_name__in=[name.split()[1] for name in member_names])

            print(f"Queryset: {queryset}")
            self.fields['to_user'].queryset = queryset # This is to set the queryset for the to_user field, which allows for the user to select the user that they want to send the request to
        else:
            self.fields['to_user'].queryset = UserProfile.objects.none()


class UpdateLaundryRequest(forms.ModelForm):

    # This is to create a field that is disabled, which makes it so that the user can't edit it
    to_user_display = forms.CharField(disabled=True, required=False, label='To User')

    class Meta:
        model = LaundryRequests
        fields = ['to_user', 'message'] # This is to set the fields that we want to use
        widgets = {'to_user': forms.HiddenInput()} # This is to hide the to_user field

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Popping the user 
        super(UpdateLaundryRequest, self).__init__(*args, **kwargs) # Calling the super class
        if self.instance and self.instance.to_user: # Checking if the instance and to_user exists
            self.fields['to_user_display'].initial = str(self.instance.to_user) # Setting the initial value for the to_user_display field

        
    

class CreateFamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name', 'family_code']
    
    # Styling
    def __init__(self, *args, **kwargs):
        super(CreateFamilyForm, self).__init__(*args, **kwargs)
        self.fields['family_name'].widget.attrs.update({
                                                        'class':'flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md', 
                                                        'placeholder':'Family Name',
                                                        'id':'family_name'}
                                                    )
        self.fields['family_code'].widget.attrs.update({
                                                        'class':'flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md', 
                                                        'placeholder':'Family Code',
                                                        'id':'family_code'}
                                                    )


class AddFamilyMembersForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100) #This is the username with max length of 100
    family_code = forms.CharField(label='Family Code', max_length=4) # This for a 4 digit family code
    
    def clean_username(self):
        username = self.cleaned_data['username'] #This is the username making sure that it is cleaned
        try:
            user = User.objects.get(username=username) #This is to get the user
            return user #This is to return the user
        except User.DoesNotExist: #This is to check if the user does not exist
            raise forms.ValidationError("Username might be incorrect") #This is to raise the error
    
    def clean_family_code(self):
        family_code = self.cleaned_data['family_code'] #This is the family code making sure that it is cleaned
        try:
            
            family = Family.objects.get(family_code=family_code) #This is to get the family
            familyCode = family.family_code #This is to get the family code
            print(familyCode)
            return familyCode #This is to return the family code
        except Family.DoesNotExist: #This is to check if the family does not exist
            raise forms.ValidationError("Family code might be incorrect") #This is to raise the error
    
    # Styling
    def __init__(self, *args, **kwargs):
        super(AddFamilyMembersForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['family_code'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})

    
    
    
        

        

    
    

    
    
    
    
    
    
    