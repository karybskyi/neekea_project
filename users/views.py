from django.shortcuts import render


def login(request):
    context = {
        "title": "Neekea - Authorisation",
    }
    return render(request, "users/login.html", context)

def logout(request):
    pass

def registration(request):
    context = {
        'title': 'Neekea - Registration',
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': 'Neekea - User Profile',
    }
    return render(request, 'users/profile.html', context)