from django.db import models
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, redirect



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
        laundry_requests = LaundryRequests.objects.filter(to_user=user)
        context['laundry_requests'] = laundry_requests
        context['relatives'] = self.object.get_siblings()
        context['children'] = self.object.children.all()
        return context


class UserListView(generic.ListView):
    model = User
    template_name = 'laundry_day/list_of_users.html'
    context_object_name = 'users'

 

def laundry_request_detail(request, from_user_id):
    from_user = User.objects.get(id=from_user_id)
    laundry_request = LaundryRequests.objects.filter(from_user=from_user)
    context = {
        'from_user': from_user,
        'laundry_request': laundry_request,
    }
    return render(request, 'laundry_day/laundry_request_detail.html', context)

def update_laundry_request(request, from_user_id, pk):
    from_user = User.objects.get(id=from_user_id)
    laundry_request = LaundryRequests.objects.get(id=pk, from_user=from_user_id)
    form = CreateLaundryRequest(instance=laundry_request)

    if request.method == 'POST':
        form = CreateLaundryRequest(request.POST, instance=laundry_request)
        if form.is_valid():
            form.save()
            return redirect('laundry_request_detail', from_user_id=laundry_request.from_user.id)

    context = {'form': form}
    return render(request, 'laundry_day/update_laundry_request.html', context)

def delete_laundry_request(request, pk):
    print(pk)
    print(request.method)
    print("in delte_laundry_request")
    laundry_request = LaundryRequests.objects.get(id=pk)
    from_user = laundry_request.from_user.id
    print(from_user)
    if request.method == 'POST':
        laundry_request.delete()
        return redirect('user_detail', pk=laundry_request.from_user.id)
    
    context = {'message': laundry_request,"from_user": from_user}
    return render(request, 'laundry_day/delete_laundry_request.html', context)

def create_laundry_request(request, pk):

    if request.method == 'POST':
        form = CreateLaundryRequest(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
        
    else:
        form = CreateLaundryRequest()  

    return render(request, 'laundry_day/create_laundry_request.html', {'form': form})

    


    


   
    


      
            