from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import loginform, signupform, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

# Constants
LOGIN_URL = "/login/"
DASHBOARD_URL = "/dashboard/"


@require_http_methods(["GET"])
def home(request):
    posts = Post.objects.all()
    return render(request, "blog/home.html", {"posts": posts})


@require_http_methods(["GET"])
def about(request):
    return render(request, "blog/about.html")


@require_http_methods(["GET"])
def contact(request):
    return render(request, "blog/contact.html")


@require_http_methods(["GET"])
@login_required
def dashboard(request):
    posts = Post.objects.all()
    return render(request, "blog/dashboard.html", {"posts": posts})


@csrf_protect
@require_http_methods(["GET", "POST"])
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


@csrf_protect
@require_http_methods(["GET", "POST"])
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
                    return HttpResponseRedirect(DASHBOARD_URL)
        else:
            fm = loginform()

        return render(request, "blog/login.html", {"form": fm})
    else:
        return HttpResponseRedirect(DASHBOARD_URL)


@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def addpost(request):
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


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def updatepost(request, id):
    pi = Post.objects.get(pk=id)
    if request.method == "POST":
        fm = PostForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        fm = PostForm(instance=pi)

    return render(request, "blog/updatepost.html", {"form": fm})


@csrf_protect
@login_required
@require_http_methods(["POST"])
def deletepost(request, id):
    pi = Post.objects.get(pk=id)
    pi.delete()
    return HttpResponseRedirect(DASHBOARD_URL)


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def changepass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return HttpResponseRedirect(DASHBOARD_URL)
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, "blog/changepass.html", {"fm": fm})
