from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import loginform, signupform, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
LOGIN_URL = "/login/"


def home(request):
    posts = Post.objects.all()

    return render(request, "blog/home.html", {"posts": posts})


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, "blog/dashboard.html", {"posts": posts})
    else:
        return HttpResponseRedirect(LOGIN_URL)


def user_signup(request):
    if request.method == "POST":
        fm = signupform(request.POST)
        if fm.is_valid():
            xxx = fm.cleaned_data["username"]

            user = fm.save()
            messages.success(request, "Account was created for " + xxx)
            group = Group.objects.get(name="auther")
            user.groups.add(group)
            return HttpResponseRedirect(LOGIN_URL)
    else:
        fm = signupform()

    return render(request, "blog/signup.html", {"form": fm})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = loginform(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data["username"]
                upass = fm.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "la moj gara")
                    return HttpResponseRedirect("/dashboard/")

        else:
            fm = loginform()

        return render(request, "blog/login.html", {"form": fm})
    else:
        return HttpResponseRedirect("/dashboard/")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def addpost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data["title"]
                desc = fm.cleaned_data["desc"]
                pst = Post(title=title, desc=desc)
                pst.save()
                fm = PostForm()
        else:
            fm = PostForm()
        return render(request, "blog/post.html", {"form": fm})
    else:
        return HttpResponseRedirect(LOGIN_URL)


def updatepost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            fm = PostForm(request.POST, instance=pi)
            if fm.is_valid():
                fm.save()
        else:
            pi = Post.objects.get(pk=id)
            fm = PostForm(instance=pi)

        return render(request, "blog/updatepost.html", {"form": fm})
    else:
        return HttpResponseRedirect(LOGIN_URL)


def deletepost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()

        return HttpResponseRedirect("/dashboard/")
    else:
        return HttpResponseRedirect(LOGIN_URL)


def changepass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return HttpResponseRedirect("/dashboard/")

    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, "blog/changepass.html", {"fm": fm})
