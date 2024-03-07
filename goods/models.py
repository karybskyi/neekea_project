from django.db import models
from django.core.validators import MaxValueValidator


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Category name")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Product name")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Photo"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Price"
    )
    discount = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(99)],
        verbose_name="Discount amount in %",
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name="Category"
    )

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("id",)

    def __str__(self) -> str:
        return f"{self.name}, {self.quantity} pcs"

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price
