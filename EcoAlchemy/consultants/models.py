# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from marketplace.models import WasteListing

class ConsultationCase(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    title = models.CharField(max_length=255)
    waste_listing = models.ForeignKey(WasteListing, on_delete=models.CASCADE, related_name='consultation_cases', null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_cases')
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_cases', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    def __str__(self):
        return self.title

class CaseComment(models.Model):
    case = models.ForeignKey(ConsultationCase, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.case.title}"