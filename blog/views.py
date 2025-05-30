from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import loginform, signupform, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# Create your views here.
LOGIN_URL = "/login/"
DASHBOARD_URL = "/dashboard/"


@require_GET
def home(request):
    posts = Post.objects.all()

    return render(request, "blog/home.html", {"posts": posts})


@require_GET
def about(request):
    return render(request, "blog/about.html")


@require_GET
def contact(request):
    return render(request, "blog/contact.html")


@login_required
@require_GET
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, "blog/dashboard.html", {"posts": posts})
    else:
        return HttpResponseRedirect(LOGIN_URL)


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


@require_http_methods(["GET", "POST"])
@csrf_protect
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


@require_POST
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
@require_http_methods(["GET", "POST"])
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


@login_required
@require_http_methods(["GET", "POST"])
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


@login_required
@require_POST
def deletepost(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()

        return HttpResponseRedirect(DASHBOARD_URL)
    else:
        return HttpResponseRedirect(LOGIN_URL)


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
