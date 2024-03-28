from django.shortcuts import render


def checkout(request):
    context = {"hide_modal_cart": True,}
    return render(request, 'orders/checkout.html', context)