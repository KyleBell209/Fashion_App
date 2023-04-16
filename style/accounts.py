from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages

def register(request):
    if request.user.is_authenticated:
        return redirect('style')
    else:
        form = CreateUserForm()
        if request.method=='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                # Create a Account instance for the new user
                Account.objects.create(user=user, name=user.username)
                messages.success(request, 'Account was created for the user, ' + form.cleaned_data.get('username'))
                return redirect('userlogin')
    context = {'form': form}
    return render(request, 'style/register.html', context=context)


def userlogin(request):
    if request.user.is_authenticated:
        return redirect('style')
    else:
        if request.method == 'POST':
            username = request.POST.get('username','')
            password = request.POST.get('password','')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('style')
            else:
                messages.info(request, 'Username or password is incorrect') 
    context = {}
    return render(request, 'style/login.html', context=context)

def userlogout(request):
    logout(request)
    return redirect('userlogin')
