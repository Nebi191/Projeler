from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.utils import timezone
# Create your models here.



class Product(models.Model):
    name = models.CharField(max_length=50) # Ürün ad
    description = models.TextField() # Açıklama
    price = models.DecimalField(max_digits=10, decimal_places=2) # Fiyat
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) #Resim
    is_popular = models.BooleanField(default=False) # Popüler mi
    is_new = models.BooleanField(default=False) # Yeni Mi
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    





class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
        
class ShippingAddress(models.Model):
    address = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.address}, {self.city}"
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Beklemede'),
        ('paid', 'Ödendi'),
        ('shipped', 'Kargolandı'),
        ('cancelled', 'İptal Edildi'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(
    ShippingAddress,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    conversation_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Sipariş #{self.pk} - {self.user.username}"
    
