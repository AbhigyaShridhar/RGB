from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.generic import View
from .models import User, Item
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def index(request):
    ctx = {
        "ranklist": User.objects.all()[:15]
    }
    return render(request, "index.html", ctx)

class RegisterView(View):
    template = "index.html"
    success_url = 'backend:index'

    def post(self, request):
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        p1 = request.POST["password"]
        p2 = request.POST["password1"]
        email = request.POST["email"]

        if not p1 == p2:
            return render(request, self.template, {
                "ranklist": User.objects.all()[:15],
                "message": "Passwords don't match!!"
            })

        if not username or not p1 or not p2 or not first_name or not last_name or not email:
            return render(request, self.template, {
                "ranklist": User.objects.all()[:15],
                "message": "Please enter all the fields!!"
            })

        try:
            user = User.objects.create_user(username, email, p1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, self.template, {
                "message": "Email address or username already taken.",
                "ranklist": User.objects.all()[:15],
            })
        login(request, user)
        return HttpResponseRedirect(reverse(self.success_url))

class LoginView(View):
    template = "index.html"
    success_url = 'backend:index'

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return render(request, self.template, {
                "ranklist": User.objects.all()[:15],
                "message": "Please enter all the fields!!"
            })

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(self.success_url))
        return render(request, self.template, {
            "ranklist": User.objects.all()[:15],
            "message": "Incorrect Username or Password!!"
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("backend:index"))

@login_required
def profile(request):
    user_items = request.user.items
    ctx = {
        "greens": user_items.filter(color="GREEN"),
        "reds": user_items.filter(color="RED"),
        "blues": user_items.filter(color="BLUE"),
    }
    return render(request, "profile.html", ctx)

@login_required
def market(request, code):
    if code == "red":
        return render(request, "red_store.html", {
            "items": Item.objects.filter(Q(color="RED") & ~Q(stock=0)),
        })
    elif code == "blue":
        return render(request, "blue_store.html", {
            "items": Item.objects.filter(Q(color="BLUE") & ~Q(stock=0)),
        })
    elif code == "green":
        return render(request, "green_store.html", {
            "items": Item.objects.filter(Q(color="GREEN") & ~Q(stock=0)),
        })
    else:
        return HttpResponse("Invalid URL!!")

def shop(request):
    return render(request, "shops.html")

@login_required
def buy(request, id, color):
    item = Item.objects.get(id=id)
    if not item.color == color:
        return HttpResponse("Invalid request!!")

    usr = request.user
    if color == "RED":
        if usr.red > item.value:
            usr.red = usr.red - item.value
            item.stock = item.stock - 1
            usr.items.add(item)
        else:
            return render(request, "red_store.html", {
                "items": Item.objects.filter(Q(color="RED") & ~Q(stock=0)),
                "message": "Invalid Funds!!",
            })
    elif color == "BLUE":
        if usr.blue > item.value:
            usr.blue = usr.blue - item.value
            item.stock = item.stock - 1
            usr.items.add(item)
        else:
            return render(request, "blue_store.html", {
                "items": Item.objects.filter(Q(color="BLUE") & ~Q(stock=0)),
                "message": "Invalid Funds!!",
            })
    elif color == "GREEN":
        if usr.green > item.value:
            usr.green = usr.blue - item.value
            item.stock = item.stock - 1
            usr.items.add(item)
        else:
            return render(request, "green_store.html", {
                "items": Item.objects.filter(Q(color="GREEN") & ~Q(stock=0)),
                "message": "Invalid Funds!!",
            })
    else:
        return HttpResponse("Invalid URL!!")

    usr.save()
    item.save()
    return HttpResponseRedirect(reverse("backend:profile"))

@login_required
def sell(request, id, color):
    item = Item.objects.get(id=id)
    if not item.color == color:
        return HttpResponse("Invalid request!!")

    usr = request.user
    if color == "RED":
        usr.red = usr.red + item.value
        item.stock = item.stock + 1
        usr.items.remove(item)

    elif color == "BLUE":
        usr.blue = usr.blue + item.value
        item.stock = item.stock + 1
        usr.items.remove(item)

    elif color == "GREEN":
        usr.green = usr.blue + item.value
        item.stock = item.stock + 1
        usr.items.remove(item)

    else:
        return HttpResponse("Invalid URL!!")

    usr.save()
    item.save()
    return HttpResponseRedirect(reverse("backend:profile"))
