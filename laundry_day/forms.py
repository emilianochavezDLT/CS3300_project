from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *

class CreateLaundryRequest(forms.ModelForm):
    class Meta:
        model = LaundryRequests
        fields = '__all__'

    


    
    
    
        

        

    
    

    
    
    
    
    
    
    