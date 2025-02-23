from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
data=datetime.now().year
def index(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        formcontainer.objects.create(name=name, email=email, phone_number=phone,message=message)
    # return render('index',{'idata': idata})

    return render(request, 'main/index.html', {'data': data})
def about(request):
    return render(request, 'main/about.html',{'data': data})
def conatct(request):
    return render(request, 'main/contact.html',{'data': data})
def menu(request):
    return render(request, 'main/menu.html',{'data': data})
def services(request):
    return render(request, 'main/services.html',{'data': data})



def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
    
        if not User.objects.filter(username=username).exists():
            messages.info(request,'Username is not found!!')
            return redirect('log_in')
        
        user=authenticate(username=username, password=password )
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'invalid keyword!!')
            return redirect('log_in')
        # formcontaioner.objects.create(name=username,password=password )
    return render(request, 'auth/login.html',)

def register(request):
    if request.method=='POST':
        first_name=request.POST['name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        # formcontainer.objects.create(email=email)

        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username is already exists!!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email is already exits!!')
                return redirect('register')
            else:
                User.objects.create_user(first_name=first_name, username=username,email=email,password=password)
                messages.success(request, 'Register Successfully!!')
                return redirect('log_in')
            
        else:
            messages.error(request, 'Password is not match.')
            return redirect('register')

    return render(request, 'auth/register.html')

def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            anchr=form.save()
            update_session_auth_hash(request,anchr)
            return redirect('log_in')
    return render(request, 'auth/change_password.html', {'form':form})

def table(request):
    data=formcontainer.objects.all()
    return render(request, 'main/table.html',{'data':data})
