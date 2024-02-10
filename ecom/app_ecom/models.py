from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Remove is_admin and is_user fields
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TodayDeal(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} - {self.date_added}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    order_note = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # other fields related to order if needed

    def __str__(self):
        return f"Order for {self.fullname} - {self.product}"
    

