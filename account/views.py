from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.contrib.auth import authenticate, login, logout

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('/auth/register/')
        
        user = User.objects.create_user(username=username, password=password)
        user.save()

        messages.info(request, "Registered Successfully")
        return redirect('/auth/register/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid username or password")
            return redirect('/auth/login/')

        login(request, user)
        return redirect('/home/all/')
    
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def logout_user(request):
    logout(request)
    messages.info(request, "Logout Successful")
    return redirect('/auth/login/')

def start(request):
    return render(request, 'start.html')

