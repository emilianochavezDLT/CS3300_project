from django.db import models
from django.shortcuts import render
from django.views import generic
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


## Notes ##
# Return redirect and render are different
# Redirect will redirect to the url, so you have to choose the url from urls.py
# Render will render the template with the context

# So, 
# If you want to redirect to the template, you have to use render
# If you want to redirect to the url, you have to use redirect

# Login required decorator will check if the user is logged in or not
# If the user is not logged in, it will redirect to the login page
# If the user is logged in, it will render the template with the context
# The decorator is either LoginRequiredMixin or @login_required
# For class view, you have to use LoginRequiredMixin and its in the leftmost paramter of the class
# For function view, you have to use @login_required and its above the function

# Your Login Url that redirects to the login page if the user is not logged in
# LOGIN_URL = reverse_lazy('login')

# Redirects to the home page if the login is successful
# LOGIN_REDIRECT_URL = reverse_lazy('user_detail') #Change this to the User Detail Page


# Create your views here #

## Index ##
def index(request):
    return render(request, 'laundry_day/index.html')


## Login, Logout, and Register ##


#This is the register view to register the user
def registerPage(request): # This is the register view to register the user
    form = CreateUserForm() # Create a form instance
    print("in registerPage") # Check if the request method is POST
    
    if request.method == 'POST': 
        print("in POST")
        form = CreateUserForm(request.POST) # Create a form instance with the submitted data
        print(form) 
        if form.is_valid(): # Check if the form is valid
            print("in valid") 
            form.save() # Save the user

            #I should change this into login in the future
            return redirect('login') # Redirect to the login page

        else:
            print("not valid") 
            print(form.errors) # Print the errors
            return render(request, 'laundry_day/register.html', {'form': form}) # Render the template with the form
    
    else:
        form = CreateUserForm() # Create a form instance
        
    context = {'form': form} # Create a context
    return render(request, 'laundry_day/register.html', context) # Render the template with the context


#This is the login function to login the user
def loginPage(request):
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data.get('username') # Cleaned (normalized) data
            password = form.cleaned_data.get('password') # Cleaned (normalized) data
            user = authenticate(request, username=username, password=password) # Authentication
            if user is not None: # If authentication was successful
                login(request, user) # Save the user and log them in
                return redirect('user_detail', pk=request.user.pk) # Redirect the userdetailpage.
            else:
                print("not valid") # If authentication failed
                form.add_error(None, 'Invalid username or password')  # Add an error to the form
    else:
        form = LoginForm() # An unbound form
    return render(request, 'laundry_day/login.html', {'form': form}) # Render our template with the form

#This is the logout function to logout the user
def logoutUser(request):
    logout(request)
    return redirect('login')



## User Related Views ##


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserProfile # This is the model that we want to use
    template_name = 'laundry_day/user_detail.html' # This is the template that we want to use
    context_object_name = 'UserProfile' # This is the context that we want to use

    # This is the context that we want to pass to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Get the context from the parent class
        user_profile = self.object # Get the user profile

        # Update the context with the user profile
        context.update({
            'laundry_requests': LaundryRequests.objects.filter(to_user=user_profile),
            'relatives': user_profile.get_siblings(),
            'children': user_profile.children.all(),
            'first_name': user_profile.user.first_name,
            'last_name': user_profile.user.last_name,
        })
        return context # Return the updated context to the template


class UserListView(LoginRequiredMixin, generic.ListView):
    model = UserProfile # This is the model that we want to use
    template_name = 'laundry_day/list_of_users.html' # This is the template that we want to use
    context_object_name = 'users' # This is the context that we want to use

 


## Laundry Request Related Views ##

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


   
    


      
            