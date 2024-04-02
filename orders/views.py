from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart
from orders.forms import CheckoutForm
from orders.models import Order, OrderedItem


def checkout(request):
    if request.method == "POST":
        form = CheckoutForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            delivery_required=form.cleaned_data["delivery_required"],
                            shipping_address=form.cleaned_data["shipping_address"],
                            payment_by_card=form.cleaned_data["payment_by_card"],
                        )
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = product.name
                            price = product.sell_price()
                            items_in_stock = product.quantity
                            items_in_cart = cart_item.quantity

                            if items_in_stock < items_in_cart:
                                raise ValidationError(
                                    f"Insufficient quantity of {name} in stock.\
                                                       Only {items_in_stock} left"
                                )

                            OrderedItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=items_in_cart,
                            )
                            items_in_stock -= items_in_cart
                            product.save()

                        cart_items.delete()

                        messages.success(request, "Your order in process!")
                        return redirect("users:profile")
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect("carts:order")

    else:
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        form = CheckoutForm(initial=initial)

    context = {
        "title": "Neekea - Checkout",
        "form": form,
        "hide_modal_cart": True,
    }
    return render(request, "orders/checkout.html", context)
