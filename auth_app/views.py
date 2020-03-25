from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html',
                      {'form': UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                # Tell the user the username is already taken
                return render(request, 'signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'That username has already been taken. Please choose a new username.'})
        else:
            # Tell the user the password didn't match
            return render(request, 'signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Passwords did not match.'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        # Login with created user
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
