from django.db import models
from account.models import CustomUser
# # Create your models here.


PAYMENT_TYPES = (
    ('MasterCard', 'MasterCard'),
    ('Visa', 'Visa')
)

# models for product category
class Category(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name',]),
        ] 

    def __str__(self):
        return self.name


# model for product color
class Color(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    rgb = models.CharField(max_length=10, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name',]),
        ] 

    def __str__(self):
        return self.name



# product model
class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='product')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'color', 'discounted_price', 'deleted']),
            models.Index(fields=['category', 'color', 'date', 'deleted'])
        ]

    def __str__(self):
        return self.title



# user basket model
class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),
        ]



class Payment(models.Model):
    type = models.CharField(max_length=16, choices=PAYMENT_TYPES)

    class Meta:
        indexes = [
            models.Index(fields=['type',]),
        ]

    def __str__(self):
        return self.type




# single order item model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.price * self.quantity



class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(OrderItem)
    address = models.CharField(max_length=256)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta:
        indexes = [
            models.Index(fields=['user',]),
        ]