from django.urls import path

from carts import views

app_name = 'carts'

# there are no media converters in paths because they'll be processed by JS
urlpatterns = [
    path('cart-add/', views.cart_add, name='cart_add'),
    path('cart-change/', views.cart_change, name='cart_change'),
    path('cart-remove/', views.cart_remove, name='cart_remove'),
]
