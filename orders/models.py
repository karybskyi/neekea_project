from django.db import models
from goods.models import Products
from users.models import User


ORDER_STATUS_CHOICES = [
        ('in_process_paid', 'Paid'),
        ('in_process', 'In Process'),
        ('сompleted ', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

class OrderQueryset(models.QuerySet):

    def total_price(self):
        return sum(order.total_order_price() for order in self)


class OrderedItemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="User",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Order placing date"
    )
    phone_number = models.CharField(max_length=20, verbose_name="Customer's phone")
    delivery_required = models.BooleanField(default=False, verbose_name="Delivery required")
    shipping_address = models.TextField(
        null=True, blank=True, verbose_name="Shipping address"
    )
    payment_by_card = models.BooleanField(default=False, verbose_name="Pay by card")
    is_paid = models.BooleanField(default=False, verbose_name="Paid already")
    status = models.CharField(
        max_length=50, 
        choices=ORDER_STATUS_CHOICES, 
        default="in_process", 
        verbose_name="Order status"
    )

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        if self.user:
            return f"Order # {self.pk} | Customer {self.user.first_name} {self.user.last_name}"
        else:
            return f"Order # {self.pk} | Customer (Unknown)"
        
    def total_order_price(self):
        return sum(item.products_price() for item in self.ordered_items.all())


class OrderedItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Order", related_name="ordered_items")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Item",
        default=None,
    )
    # backup item's title in case of deleting product from db and setting it to Null
    name = models.CharField(max_length=150, verbose_name="Item's title")
    price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Final price"
    )
    quantity = models.PositiveBigIntegerField(default=0, verbose_name="Quantity")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Order date"
    )

    class Meta:
        db_table = "ordered item"
        verbose_name = "Ordered item"
        verbose_name_plural = "Ordered items"

    objects = OrderedItemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self) -> str:
        return f"Item {self.name} | Order # {self.order.pk}"
