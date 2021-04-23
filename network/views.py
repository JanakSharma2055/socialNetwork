from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User,Follower,Post,Likes
from django.http.response import JsonResponse
import json


def index(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        # Attempt to sign user in
        content = request.POST["content"]
        Post.objects.create(post=content, user=request.user)
        return HttpResponseRedirect(reverse("index"))

    else:
        all_posts = Post.objects.all().order_by("-post_date")
        paginator = Paginator(all_posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "page_obj": page_obj
        })

@csrf_exempt
def editPost(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    if request.method !="POST":
        return JsonResponse({"error": "Post method required."}, status=400)

    data = json.loads(request.body)
    p_id=data.get("val")
    old_post=Post.objects.get(id=p_id)
    print(old_post)
    edited_content=data.get("post_Content")
    if edited_content:
        old_post.post=edited_content
    
    old_post.save()


    #print(data["post_Content"])
    return JsonResponse({"message":"successs"},status=200)


def profileView(request,user_name):
    is_followed = False
    user_details = User.objects.get(username=user_name)
    post_by_user=user_details.posts.order_by("-post_date").all()
    print("from profile")
    print(post_by_user)
    print(user_details)
    if request.method == "POST":
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login'))

            if "unfollow_btn" in request.POST:
                Follower.objects.get(user=user_details, follower=request.user).delete()
            elif "follow_btn" in request.POST:
                Follower.objects.create(user=user_details, follower=request.user)
            else:
                print("Error: wrong input name")
            return HttpResponseRedirect(reverse("profile", args=(user_name, )))
    
    if request.user.is_authenticated:
        is_followed = request.user.followee.filter(user=user_details.id).exists()
    return render(request,"network/profile.html",
    {"user_details":user_details,
    "posts":post_by_user,
    "following_status":is_followed
    })
    
def Following(request):
    user=User.objects.get(id=request.user.id)
    print("debugging from following-----------------------")
    print(user)
    followed_users_from_followers=user.followee.filter(follower=user)
    print(followed_users_from_followers)
    followed_users=[]
    for item in followed_users_from_followers:
        print(item.user)
        followed_users.append(item.user)
    print("from following:")
    print(followed_users)
    
    posts = Post.objects.filter(user__in=followed_users).order_by("-post_date")
    return render(request, "network/index.html", {
            "post_data": posts
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
