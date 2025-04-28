# marketplace/forms.py
from django import forms
from .models import WasteListing, Product

class WasteListingForm(forms.ModelForm):
    # Remove images from the ModelForm since it's handled separately
    class Meta:
        model = WasteListing
        fields = ['title', 'category', 'description', 'quantity', 'unit', 'location', 
                  'price', 'is_free', 'potential_uses', 'hazard_level']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_free'].help_text = 'Check this if you are offering this waste for free.'
        if self.instance and self.instance.is_free:
            self.fields['price'].widget = forms.HiddenInput()

class ProductForm(forms.ModelForm):
    # Remove images from the ModelForm since it's handled separately
    class Meta:
        model = Product
        fields = ['title', 'description', 'waste_source', 'price', 'quantity_available']