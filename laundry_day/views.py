from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import *

# Create your views here.
def index(request):
    return render(request, 'laundry_day/index.html')

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'laundry_day/user_detail.html'