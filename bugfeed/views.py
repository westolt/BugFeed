from django.http import HttpResponse, JsonResponse
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

# A01:2021-Broken Access Control
def deleteView(request, post_id):
    post = FeedItem.objects.get(id=post_id)
    
    post.delete()

    return redirect('/')

# HOW TO FIX "Broken Access Control":

# def deleteView(request, post_id):
#     post = FeedItem.objects.get(id=post_id)
    
#     if post.owner != request.user:
#          return HttpResponse('Access denied')
    
#     post.delete()

#     return redirect('/')

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

# A07:2021 – Identification and Authentication Failures
def signupView(request):
    if request.method == 'POST':
        username = request.POST['username']
        p1 = request.POST['password1']
        p2 = request.POST['password2']

        if p1 != p2:
            return HttpResponse('Passwords are not the same!')
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already taken!')
        
        user = User.objects.create_user(username=username, password=p1)
        login(request, user)
        return redirect('/')
    
    return redirect('login')

# HOW TO FIX "Identification and Authentication Failures":

# def signupView(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         p1 = request.POST['password1']
#         p2 = request.POST['password2']

#         if p1 != p2:
#             return HttpResponse('Passwords are not the same!')
#         if User.objects.filter(username=username).exists():
#             return HttpResponse('Username already taken!')

#         if len(p1) < 10 or p1.isalpha() or p1.isdigit() or p1.islower() or p1.isupper():
#             return HttpResponse("Password too weak")
#         else:
#             user = User.objects.create_user(username=username, password=p1)
#             login(request, user)
#             return redirect('/')
    
#     return redirect('login')

def logoutView(request):
	logout(request)
	return redirect('/login')

def infoView(request):
    posts = FeedItem.objects.all()
    data = []
    
    for post in posts:
        data.append({
            'id': post.id,
            'owner': post.owner.username,
            'content': post.content,
            'date': post.pub_date,
            'likes_count': post.likes.count(),
            'liked_by': [user.username for user in post.likes.all()],
        })

    return JsonResponse(data, safe=False)