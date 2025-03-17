from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User,Posts,Follow


def index(request):
    posts=Posts.objects.all().order_by('-timestamp')

    paginator=Paginator(posts,10)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)

    return render(request, "network/index.html",{
        "posts":page_obj
    })

@csrf_exempt
@login_required
def toggle_like(request):
    liked=None
    if request.method=="POST":
        data=json.loads(request.body)
        post_id=data.get('post_id')
        try:
            post=Posts.objects.get(id=post_id)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                liked=False

            else:
                post.likes.add(request.user)
            return JsonResponse({
                "success":True,
                "liked":liked,
                "likes_count":post.likes.count()
            })
        except post.DoesNotExist:
            return JsonResponse({
                "success":False,
                "message":"Page Not Found"
            },status=404)
    else:
        return JsonResponse({
            "message":"Invalid Response Method",

        },status=400)

@csrf_exempt
@login_required
def edit_post(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get('post_id')
        new_content = data.get('content')
        try:
            post = Posts.objects.get(user=request.user, id=post_id)
            post.content = new_content
            post.save()
            return JsonResponse({"success": "true", "message": "Post updated successfully!"})
        except Posts.DoesNotExist:
            return JsonResponse({"success": "false", "message": "Post not found or you are not authorized to edit it."}, status=404)
    return JsonResponse({"message": "Invalid method"}, status=400)


@login_required
def following(request):
    user=request.user
    user_follows=Follow.objects.filter(follower=user)
    following=user_follows.values_list('following',flat=True)
    posts=Posts.objects.filter(user__in=following).order_by('-timestamp')

    paginator=Paginator(posts,10)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)

    return render(request,"network/following.html",{
        "posts":page_obj,
    })

@login_required
def newpost(request):
    if request.method=="POST":
        content=request.POST["content"]
        if content and content.strip():
            Posts.objects.create(user=request.user,content=content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"network/newpost.html",{
                "message":"The content Field should not be empty"
            })
    return render(request,"network/newpost.html")

@login_required
def profile(request, user_id):
    try:
        profile_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")


    followers = Follow.objects.filter(following=profile_user).count()
    following = Follow.objects.filter(follower=profile_user).count()
    posts = Posts.objects.filter(user=profile_user).order_by('-timestamp')

    paginator=Paginator(posts,10)
    page_num=request.GET.get('page')
    page_obj=paginator.get_page(page_num)
    button = None
    if request.user != profile_user:

        if not Follow.objects.filter(follower=request.user, following=profile_user).exists():
            button = "Follow"
        else:
            button = "UnFollow"

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "followers": followers,
        "following": following,
        "posts": page_obj,
        "button": button
    })

@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST.get("profile_user")
        button_val = request.POST.get("button_value")
        profile_user = get_object_or_404(User, id=user_id)

        # Toggle follow status
        if button_val == "Follow":
            Follow.objects.create(follower=request.user, following=profile_user)
            messages.success(request, f"Congratulations! You are now following {profile_user.username}")
            button = "UnFollow"
        elif button_val == "UnFollow":
            Follow.objects.filter(follower=request.user, following=profile_user).delete()
            messages.success(request, f"Done! You are now not following {profile_user.username}")
            button = "Follow"


        followers = Follow.objects.filter(following=profile_user).count()
        following = Follow.objects.filter(follower=profile_user).count()
        posts = profile_user.posts.all()
        paginator=Paginator(posts,10)
        page_num=request.GET.get('page')
        page_obj=paginator.get_page(page_num)
        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "followers": followers,
            "following": following,
            "posts": page_obj,
            "button": button
        })
    else:
        return HttpResponseRedirect(reverse("index"))

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
