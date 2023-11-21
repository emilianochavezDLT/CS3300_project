from django.db import models
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    return render(request, 'laundry_day/index.html')

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile
    template_name = 'laundry_day/user_detail.html'
    context_object_name = 'UserProfile'

    # This is the context that we want to pass to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.object

        context.update({
            'laundry_requests': LaundryRequests.objects.filter(to_user=user_profile),
            'relatives': user_profile.get_siblings(),
            'children': user_profile.children.all(),
            'first_name': user_profile.user.first_name,
            'last_name': user_profile.user.last_name,
        })
        return context


class UserListView(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = 'laundry_day/list_of_users.html'
    context_object_name = 'users'

 
@login_required
def laundry_request_detail(request, from_user_id):
    from_user = UserProfile.objects.get(id=from_user_id)
    laundry_request = LaundryRequests.objects.filter(from_user=from_user)
    context = {
        'from_user': from_user,
        'laundry_request': laundry_request,
    }
    return render(request, 'laundry_day/laundry_request_detail.html', context)


@login_required
def update_laundry_request(request, from_user_id, pk):
    from_user = UserProfile.objects.get(id=from_user_id)
    laundry_request = LaundryRequests.objects.get(id=pk, from_user=from_user_id)
    form = CreateLaundryRequest(instance=laundry_request)

    if request.method == 'POST':
        form = CreateLaundryRequest(request.POST, instance=laundry_request)
        if form.is_valid():
            form.save()
            return redirect('laundry_request_detail', from_user_id=laundry_request.from_user.id)

    context = {'form': form}
    return render(request, 'laundry_day/update_laundry_request.html', context)


@login_required
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

@login_required 
def create_laundry_request(request, pk):

    if request.method == 'POST':
        form = CreateLaundryRequest(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
        
    else:
        form = CreateLaundryRequest()  

    return render(request, 'laundry_day/create_laundry_request.html', {'form': form})

def registerPage(request):
    form = CreateUserForm()
    print("in registerPage")
    
    if request.method == 'POST':
        print("in POST")
        form = CreateUserForm(request.POST)
        print(form)
        if form.is_valid():
            print("in valid")
            form.save()

            #I should change this into login in the future
            return render(request, 'laundry_day/index.html')

        else:
            print("not valid")
            print(form.errors)
            return render(request, 'laundry_day/register.html', {'form': form})
    
    else:
        form = CreateUserForm()
        
    context = {'form': form}
    return render(request, 'laundry_day/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the index page or your desired page
            else:
                # Even though the form is technically valid, authentication has failed
                form.add_error(None, 'Invalid username or password')  # Add a non-field error
    else:
        form = LoginForm()
    return render(request, 'laundry_day/login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')
    


   
    


      
            