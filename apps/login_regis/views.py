from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

def index(request):
    if id in request.session:
        request.session.clear()

    return render(request, 'login_regis/index.html')

def process(request):
    x = User.objects.register(request.POST)
    if x[0] == True:
        messages.success(request, "Registration Successful")
    else:
        for error in x[1]:
            messages.error(request, error)
    return redirect("/")

def login(request):
    y = User.objects.login(request.POST)

    if y[0] == True:
        # print y[2]
        # print User.objects.get(id=y[2])
        # print User.objects.get(id=y[2]).first_name
        # print User.objects.get(id=y[2]).last_name
        # context = {
        #     "logged_in_user" : User.objects.get(id=y[2])
        # }
        # messages.success(request, "Login Successful")
        request.session["id"] = y[2]
        return redirect("/success")
    else:
        for error in y[1]:
            messages.error(request, error)
        return redirect("/")

def success(request):
    print request.session["id"]
    context = {
        "names" : User.objects.get(id=request.session["id"])
    }
    return render(request, "login_regis/success.html", context)

def logout(request):
    return redirect("/")

def error(request):
    return redirect("/")
