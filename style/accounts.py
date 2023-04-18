from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages

def register(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('style')
    else:
        # Initialize a new instance of the CreateUserForm
        form = CreateUserForm()
        if request.method=='POST':
            # Validate the form data
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Create a Account instance for the new user
                Account.objects.create(user=user, name=user.username)
                messages.success(request, 'Account was created for the user, ' + form.cleaned_data.get('username'))
                return redirect('userlogin')
            # Return the rendered HTML template
    context = {'form': form}
    return render(request, 'style/register.html', context=context)



def userlogin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('style')
    else:
        if request.method == 'POST':
            username = request.POST.get('username','')
            password = request.POST.get('password','')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log in the user and redirect them to the home page
                login(request, user)
                return redirect('style')
            else:
                messages.info(request, 'Username or password is incorrect') 
    # Return the rendered HTML template
    context = {}
    return render(request, 'style/login.html', context=context)


def userlogout(request):
    # Log out the user and redirect them to the login page
    logout(request)
    return redirect('userlogin')

