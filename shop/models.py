from uuid import uuid4
from django.core.validators import MinValueValidator
from django.db import models
from account.models import User
from .validators import image_maximum_file_size
from rest_framework import reverse
from rest_framework.response import Response


class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Collection(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='featured')

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    inventory = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotion = models.ManyToManyField(Promotion, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sold_number = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse.reverse('shop:products-detail-with-slug', args=[str(self.id), str(self.slug)])

    class Meta:
        permissions = [('edit_product', 'can edit product')] #this permission allows sellers to edit or delete their own products, checkout permissions.py

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[image_maximum_file_size])

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
        (PAYMENT_STATUS_COMPLETED, 'Completed')
    ]
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)    

    def __str__(self) -> str:
        return f'{self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.order}'


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    class Meta:
        unique_together = [['cart', 'product']]

class Review(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=800)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')