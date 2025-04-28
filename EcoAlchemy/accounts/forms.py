from django import forms
from .models import UserProfile, IndustryApplication

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'address', 'phone']
        
class IndustryApplicationForm(forms.ModelForm):
    class Meta:
        model = IndustryApplication
        fields = ['company_name', 'industry_type', 'registration_number']