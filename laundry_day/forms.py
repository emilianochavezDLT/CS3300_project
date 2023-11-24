from typing import Any
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#We are going to create new user form
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name', 
                  'username', 
                  'password1', 
                  'password2'
                ]
        

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

    
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
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['last_name'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['password1'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['password2'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist")
        return username
    
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is None:
            raise forms.ValidationError("Username is required.")
        user = User.objects.filter(username=username).first()
        if user is None:
            raise forms.ValidationError("Username does not exist.")
        if not user.check_password(password):
            raise forms.ValidationError("Password is incorrect")
        return password
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['password'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})

#This is to create a laundry request
class CreateLaundryRequest(forms.ModelForm):
    class Meta:
        model = LaundryRequests
        fields = ['to_user', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(CreateLaundryRequest, self).__init__(*args, **kwargs)
        if user:
            self.fields['to_user'].queryset = User.objects.filter(family=user.families)
        else:
            self.fields['to_user'].queryset = User.objects.none()


class CreateFamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name', 'family_code']
        
    def __init__(self, *args, **kwargs):
        super(CreateFamilyForm, self).__init__(*args, **kwargs)
        self.fields['family_name'].widget.attrs.update({
                                                        'class':'flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md', 
                                                        'placeholder':'Family Name'}
                                                    )
        self.fields['family_code'].widget.attrs.update({
                                                        'class':'flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md', 
                                                        'placeholder':'Family Code'}
                                                    )


class AddFamilyMembersForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    family_code = forms.CharField(label='Family Code', max_length=4)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            raise forms.ValidationError("Username might be incorrect")
    
    def clean_family_code(self):
        family_code = self.cleaned_data['family_code']
        try:
            
            family = Family.objects.get(family_code=family_code)
            familyCode = family.family_code
            print(familyCode)
            return familyCode
        except Family.DoesNotExist:
            raise forms.ValidationError("Family code might be incorrect")
    
    def __init__(self, *args, **kwargs):
        super(AddFamilyMembersForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})
        self.fields['family_code'].widget.attrs.update({'class':'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'})

    
    
    
        

        

    
    

    
    
    
    
    
    
    