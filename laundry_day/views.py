from django.db import models
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from django.views import generic
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
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
        laundry_requests = LaundryRequests.objects.filter(from_user=user)
        context['laundry_requests'] = laundry_requests
        context['relatives'] = self.object.get_siblings()
        context['children'] = self.object.children.all()
        return context
    

def laundry_request_detail(request, from_user_id):
    laundry_request = LaundryRequests.objects.get(from_user_id=from_user_id)
    print(laundry_request)
    return render(request, 'laundry_day/laundry_request_detail.html', {'laundry_request': laundry_request})


def create_laundry_request(request, pk):

    if request.method == 'POST':
        form = CreateLaundryRequest(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
        # Do not re-initialize the form here, because this will erase the errors and data
    else:
        form = CreateLaundryRequest()  # Initialize a new form for a GET request

    return render(request, 'laundry_day/create_laundry_request.html', {'form': form})

    


    


   
    


      
            