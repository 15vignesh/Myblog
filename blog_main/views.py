from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from blogs.models import Category,Blog,Security
from assignments.models import About
from .forms import RegistrationForm,SecurityCheckForm,ForgotPasswordForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib import auth,messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

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
            form.errors.clear()
            messages.error(request, "Invalid Username or Password")
    else:
        form=AuthenticationForm()
    context={
        'form':form,
    }
    return render(request,'login.html',context)

def forgot(request):
    if request.method=='POST':
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            username_or_email=form.cleaned_data.get('username_or_email')
            try:
                user=User.objects.get(username=username_or_email) or User.objects.get(email=username_or_email)
                security=Security.objects.get(user=user)
                request.session['user_id']=user.id
                return redirect('security_check')
            except User.DoesNotExist:
                messages.error(request,"No User found with this username or email.")
            except Security.DoesNotExist:
                messages.error(request,"Security information not found.")
    else:
        form=ForgotPasswordForm()
    context={
        'form':form,
    }
    return render(request,'forgot.html',context)

def security_check(request):
    if 'user_id' not in request.session:
        return redirect('forgot')
    user=get_object_or_404(User,id=request.session.get('user_id'))
    security=get_object_or_404(Security,user=user)
    
    if request.method=='POST':
        form=SecurityCheckForm(request.POST)
        if form.is_valid():
            question=form.cleaned_data.get('security_question')
            answer=form.cleaned_data.get('security_answer')
            
            if question.lower()==security.security_question.lower() and security.check_security_answer(answer):
                return redirect('reset_password')
            else:
                messages.error(request," Security Question or Answer is Incorrect.")
    else:
        form=SecurityCheckForm()
    context={
        'form':form,
    }
        
    return render(request,'security_check.html',context)

def reset_password(request):
    if 'user_id' not in request.session:
        return redirect('forgot')
    user=get_object_or_404(User,id=request.session.get('user_id'))
    
    if request.method=='POST':
        form=SetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            del request.session['user_id']
            return render(request, 'password_change.html', {'form': form, 'success': True})
    else:
        form=SetPasswordForm(user)
    context={
        'form':form,
    }
    return render(request,'password_change.html',context)
def logout(request):
    auth.logout(request)
    return redirect('home')