from typing import Any
from django import forms
from blogs.models import Category,Blog,Security
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'
        
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=('title','category','featured_image','short_description','blog_body','status','is_featured')
        

class AddUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','is_active','is_staff','is_superuser','groups','user_permissions')
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields.pop('usable_password',None)
        
class EditUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','email','first_name','last_name','is_active','is_staff','is_superuser','groups','user_permissions')

class SecurityQuestionForm(forms.ModelForm):
    class Meta:
        model=Security
        fields=('security_question','security_answer')
        widgets={
            'security_answer': forms.PasswordInput(), 
        }