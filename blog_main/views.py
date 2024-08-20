from django.shortcuts import render,redirect
from blogs.models import Category,Blog
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth,messages
from django.contrib.auth import authenticate, login as auth_login


def home(request):
    featured_posts=Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts=Blog.objects.filter(is_featured=False, status='Published')
    
    # fetch about me
    try:
        about=About.objects.get()
    except:
        about=None
    context={
        'featured_posts':featured_posts,
        'posts':posts,
        'about':about,
    }
    return render(request,'home.html',context)

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('register')
        else:
            messages.error(request, "Registration Failed.Try again.")

    else:
        form=RegistrationForm()
    context={
        'form':form,
        }
    return render(request,'register.html',context)

def login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid Username or Password")
    else:
        form=AuthenticationForm()
    context={
        'form':form,
    }
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('home')