from django.db import models

from accounts.models import User
from products.models import ProductModel

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("canceled", "Canceled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="pending")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.phone}"

    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.order.user.full_name}'

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='address')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    province = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=11, unique=True, db_index=True)
    postal_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.phone_number}'
    
    def clean_data(self):
        city = self.cleaned_data.get('city')
        province = self.cleaned_data.get('province')
        postal_code = self.cleaned_data.get('postal_code')
        
        for field_name, value in [('city', city), ('province', province), ('postal_code', postal_code)]:
            if not value:
                raise ValueError(f"Please fill the {field_name} field")
        
        return city, province, postal_code