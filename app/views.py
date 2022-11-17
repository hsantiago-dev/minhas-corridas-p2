from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import User


def index(request):
    return render(request, 'index.html')


def registration_user(request):
    return render(request, 'registration_user.html')


def login(request):
    return render(request, 'login.html')


def insert_user(request):
    if request.POST['name'] and request.POST['email'] and request.POST['password']:
        user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
        user.name = request.POST['name']
        user.save()
        return redirect('login')

    return redirect('registration_user')


@login_required
def interested_races(request):
    return render(request, 'interested_races.html')


@login_required
def registered_races(request):
    return render(request, 'registered_races.html')


@login_required
def races_created(request):
    return render(request, 'races_created.html')
