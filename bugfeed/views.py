from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from .models import FeedItem

def homePageView(request):
	posts = FeedItem.objects.all().order_by('-pub_date')
	context = {"posts": posts}
	return render(request, 'pages/index.html', context)

def addView(request):
    if request.method == 'POST':
        user = request.user
        content = request.POST["content"]
        FeedItem.objects.create(owner = user, content=content)
    return redirect('/')

def likeView(request, post_id):
    post = FeedItem.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    return redirect('/')

def deleteView(request, post_id):
    post = FeedItem.objects.get(id=post_id)
    user = request.user
    
    if post.owner == user:
         print(post)
         post.delete()

    return redirect('/')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse('Invalid credentials')
    return render(request, 'pages/login.html')

def logoutView(request):
	logout(request)
	return redirect('/login')