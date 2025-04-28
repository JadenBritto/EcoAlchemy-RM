# marketplace/models.py
from django.db import models
from django.contrib.auth.models import User  # Correct import for User

class WasteCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Waste Categories"

class WasteListing(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('pending', 'Pending Transaction'),
        ('completed', 'Transaction Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_listings')
    title = models.CharField(max_length=255)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE, related_name='listings')
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    potential_uses = models.TextField(blank=True, null=True)
    hazard_level = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    def __str__(self):
        return self.title
    
    def mark_as_completed(self):
        self.status = 'completed'
        self.save()
        # Award Green Credits to the user
        self.user.profile.green_credits += 10
        self.user.profile.save()

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    waste_source = models.ForeignKey(WasteCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class WasteImage(models.Model):
    waste_listing = models.ForeignKey(WasteListing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='waste_images/')
    
    def __str__(self):
        return f"Image for {self.waste_listing.title}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.title}"