import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
    if request.method=='POST':
        new_post=Post(username=request.user.username, content=request.POST['post_content'])
        new_post.save()
        return HttpResponseRedirect(reverse('network:index'))
    liked_data=Like.objects.all()
    if request.user.username in liked_data.values_list('user', flat=True):
        user_likes=Like.objects.filter(user=request.user.username)
        post=Post.objects.filter().order_by('-date')
        paginator = Paginator(post, 10)
        page_num = request.GET.get('page')
        page_item = paginator.get_page(page_num)
        return render(request, "network/index.html", {
        'post':page_item,
        'liked_posts':user_likes.values_list('post', flat=True)
        })
    post=Post.objects.filter().order_by('-date')
    paginator = Paginator(post, 10)
    page_num = request.GET.get('page')
    page_item = paginator.get_page(page_num)
    return render(request, "network/index.html", {
    'post':page_item,
    })


def following(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            new_following=User_Following(user=request.user.username, username=request.POST['username'])
            new_following.save()
            user_posts=Post.objects.filter(username=request.POST['username'])
            for i in user_posts:
                new_post_following=Post_Following(user=request.user.username, username=i.username, content=i.content, date=i.date, like=i.like)
                new_post_following.save()
            user=User.objects.get(username=request.POST['username'])
            user.followers=(user.followers+1)
            user.save()
            this_user=User.objects.get(username=request.user.username)
            this_user.following=(user.following+1)
            this_user.save()
            return HttpResponseRedirect(reverse('network:following'))
        post=Post_Following.objects.filter(user=request.user.username).order_by('-date')
        paginator = Paginator(post, 10)
        page_num = request.GET.get('page')
        page_item = paginator.get_page(page_num)
        return render(request, "network/following.html", {
        'post':page_item
        })
    else:
        return HttpResponseRedirect(reverse('network:login'))

def unfollow(request):
    if request.method=='POST':
        delete_follow=Post_Following.objects.filter(user=request.user.username, username=request.POST['username'])
        delete_follow.delete()
        delete_user_following=User_Following.objects.filter(user=request.user.username, username=request.POST['username'])
        delete_user_following.delete()
        user=User.objects.get(username=request.POST['username'])
        if (user.followers!=0):
            user.followers=(user.followers-1)
            user.save()
        this_user=User.objects.get(username=request.user.username)
        if (this_user.following!=0):
            this_user.following=(this_user.following-1)
            this_user.save()

        return HttpResponseRedirect(reverse('network:following'))

def profile(request):
    post=Post.objects.filter(username=request.user.username).order_by('-date')
    paginator = Paginator(post, 10)
    page_num = request.GET.get('page')
    page_item = paginator.get_page(page_num)
    return render(request, "network/profile.html", {
    'profile_user':User.objects.get(username=request.user.username),
    'post':page_item,
    'actual_user':request.user.username,
    })

def posts(request):
    posts=Post.objects.all().order_by('-date')
    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
@login_required
def get_post(request, post_id):
    post = Post.objects.get(username=request.user.username, pk=post_id)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content", "")
        post.content=content
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def like(request, post_id):
    post = Post.objects.get(username=request.user.username, pk=post_id)
    post_liked=Like.objects.get(user=request.user.username)
    if request.method == "PUT":
        data = json.loads(request.body)
        like = data.get("like", "")
        liked_post = data.get("liked_post", "")
        post.like=like
        post_liked.post.add(liked_post)
        post.save()
        post_liked.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def unlike(request, post_id):
    post = Post.objects.get(username=request.user.username, pk=post_id)
    post_liked=Like.objects.get(user=request.user.username)
    if request.method == "PUT":
        data = json.loads(request.body)
        like = data.get("like", "")
        liked_post = data.get("liked_post", "")
        post.like=like
        post_liked.post.remove(liked_post)
        post.save()
        post_liked.save()
        return HttpResponse(status=204)


def other_user_profile(request):
    check_user=User_Following.objects.filter(user=request.user.username)
    check_user_list=check_user.values_list('username', flat=True)
    return render(request, "network/profile.html", {
    'profile_user':User.objects.get(username=request.GET['username']),
    'post':Post.objects.filter(username=request.GET['username']).order_by('-date'),
    'actual_user':request.user.username,
    'check_user_list':check_user_list
    })
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        Like.objects.create(user=request.user.username)

        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
