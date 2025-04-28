from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from marketplace.models import WasteListing, Product

def home(request):
    top_waste_listings = WasteListing.objects.filter(status='available').order_by('-created_at')[:6]
    top_products = Product.objects.all().order_by('-created_at')[:6]
    
    context = {
        'top_waste_listings': top_waste_listings,
        'top_products': top_products,
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    user = request.user
    user_profile = user.profile
    
    context = {
        'user_profile': user_profile,
    }
    
    # Add context based on user type
    if user_profile.user_type == 'industry':
        context['waste_listings'] = WasteListing.objects.filter(user=user).order_by('-created_at')
        context['products'] = Product.objects.filter(user=user).order_by('-created_at')
    elif user_profile.user_type == 'consultant':
        context['assigned_cases'] = user.assigned_cases.all().order_by('-created_at')
    
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')
# Create your views here.
