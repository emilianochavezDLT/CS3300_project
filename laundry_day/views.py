from typing import Any
from django.db import models
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from django.views import generic
from .models import *

# Create your views here.
def index(request):
    return render(request, 'laundry_day/index.html')

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'laundry_day/user_detail.html'
    context_object_name = 'user'

    # This is the context that we want to pass to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['relatives'] = self.object.get_siblings()
        context['children'] = self.object.children.all()
        return context
    
    

      
            