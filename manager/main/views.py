from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model


def login_view(request):
    if(request.user.is_authenticated):
        return redirect("managervideo:dashboard")
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("managervideo:dashboard")
            else:
                messages.error(request, "Wrong password!")
        except:
            messages.error(request, "User is not exist!")

    return render(request, 'login.html', context)

@login_required(login_url='/login')
def logoutPage(request):
    logout(request)
    return redirect('/')


def forgotPassword(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return redirect('/')
    except:
         messages.error(request, "User is not exist!")
    return render(request, 'forgotpassword.html', context)
