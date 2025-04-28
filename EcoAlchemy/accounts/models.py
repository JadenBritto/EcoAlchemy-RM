# from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('industry', 'Industry'),
        ('consultant', 'Consultant'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    green_credits = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

class IndustryApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='industry_applications')
    company_name = models.CharField(max_length=255)
    industry_type = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.status}"