from django.contrib import admin

from orders.models import Order, OrderedItem

class OrederedItemsTabAdmin(admin.TabularInline):
    model = OrderedItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )

    extra = 0

class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = (
        "order_info",
        "delivery_required",
        "status",
        "payment_by_card",
        "is_paid",
        "created_timestamp",
    )

    readonly_fields = ("order_info", "created_timestamp")
    extra = 0

    def order_info(self, obj):
        return str(obj)

    order_info.short_description = "Order Info"


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "delivery_required",
        "status",
        "payment_by_card",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "delivery_required",
        "status",        
        "payment_by_card",
        "is_paid",
        )
    inlines = (OrederedItemsTabAdmin,)