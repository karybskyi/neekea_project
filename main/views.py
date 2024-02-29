from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        "title": "Neekea - main page", 
        "body_class_name": "index-body",
        "header": "NEEKEA furniture store"
        }

    return render(request, "main/index.html", context)


def about(request):
    context = {
        "title": "Neekea - about us",
        "header": "About us",
        "text_on_page": "About usAbout usAbout usAbout usAbout usAbout usAbout us"
        }

    return render(request, "main/about.html", context)
