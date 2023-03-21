from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

def login(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        return redirect('Home')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("Home")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("Home")

def register(request):
    currentUser = request.user
    if currentUser.is_authenticated:
        return redirect('Home')
    if request.POST:
        fname = request.POST.get('f_name')
        lname = request.POST.get('l_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password1')

        if pass1 != pass2:
            messages.error(request, "Password doesn't match")
            return redirect('register')
        elif User.objects.filter(email=email) or User.objects.filter(username=username):
            messages.error(request, "Username or Email Already Taken")
            return redirect('register')
        else:
            user = User.objects.create_user(email=email, username=username, first_name=fname, last_name=lname, password=pass1)
            auth.login(request, user)
            return redirect('Home')

    return render(request, "registration.html")
