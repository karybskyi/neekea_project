from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from carts.models import Cart
from orders.models import Order, OrderedItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(
                    request,
                    mark_safe(f"You're logged in as <strong>{username}</strong>"),
                )

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("user:logout"):
                    return HttpResponseRedirect(request.POST.get("nextPOST"))

                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "Neekea - Authorisation",
        "form": form,
    }
    return render(request, "users/login.html", context)


@login_required
def logout(request):
    messages.success(
        request,
        mark_safe(f"<strong>{request.user.username}</strong>, you've been logged out"),
    )
    auth.logout(request)
    return redirect(reverse("users:login"))


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(
                request,
                mark_safe(
                    f"You're registered and logged in as <strong>{user.username}</strong>"
                ),
            )

            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Neekea - Registration",
        "form": form,
    }
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile data has been updated")
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "ordered_items",
                queryset=OrderedItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    context = {
        "title": "Neekea - User Profile",
        "form": form,
        "hide_modal_cart": True,
        "orders": orders,
    }
    return render(request, "users/profile.html", context)


def users_cart(request):
    return render(
        request,
        "users/users_cart.html",
        {
            "hide_modal_cart": True,
        },
    )
