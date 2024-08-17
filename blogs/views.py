from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Category,Blog


def posts_by_category(request,category_id):
    # Fetch the post that belongs to the category with the id category_id
    posts=Blog.objects.filter(status='Published',category=category_id)
    # use try and catch when we want to do some custom action if category does not exist
    # try:
    #     category=Category.objects.get(pk=category_id)
    # except:
    #     return redirect('home')
    
    category=get_object_or_404(Category,pk=category_id)
    context={
        'posts':posts,
        'category':category,
    }
    return render(request,'posts_by_category.html',context)