from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WasteListing, Product, WasteCategory ,WasteImage, ProductImage
from .forms import WasteListingForm, ProductForm
from django.core.mail import send_mail
from django.conf import settings

def waste_list(request):
    categories = WasteCategory.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        waste_listings = WasteListing.objects.filter(
            status='available',
            category__id=selected_category
        ).order_by('-created_at')
    else:
        waste_listings = WasteListing.objects.filter(status='available').order_by('-created_at')
    
    context = {
        'waste_listings': waste_listings,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'marketplace/waste_list.html', context)

def waste_detail(request, pk):
    waste_listing = get_object_or_404(WasteListing, pk=pk, status='available')
    related_waste = WasteListing.objects.filter(
        category=waste_listing.category, 
        status='available'
    ).exclude(pk=pk)[:4]
    
    context = {
        'waste_listing': waste_listing,
        'related_waste': related_waste,
    }
    return render(request, 'marketplace/waste_detail.html', context)

@login_required
def create_waste_listing(request):
    if request.user.profile.user_type != 'industry':
        messages.error(request, 'Only industries can create waste listings.')
        return redirect('waste_list')
    
    if request.method == 'POST':
        form = WasteListingForm(request.POST)
        if form.is_valid():
            waste_listing = form.save(commit=False)
            waste_listing.user = request.user
            waste_listing.save()
            
            # Handle multiple image uploads directly
            if 'images' in request.FILES:
                for image in request.FILES.getlist('images'):
                    WasteImage.objects.create(waste_listing=waste_listing, image=image)
            
            messages.success(request, 'Waste listing created successfully!')
            return redirect('waste_detail', pk=waste_listing.pk)
    else:
        form = WasteListingForm()
    
    return render(request, 'marketplace/create_waste_listing.html', {'form': form})

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
    }
    return render(request, 'marketplace/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        waste_source=product.waste_source
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'marketplace/product_detail.html', context)

@login_required
def create_product(request):
    if request.user.profile.user_type != 'industry':
        messages.error(request, 'Only industries can create products.')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            
            # Handle multiple image uploads directly
            if 'images' in request.FILES:
                for image in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product created successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    
    return render(request, 'marketplace/create_product.html', {'form': form})

@login_required
def contact_waste_owner(request, pk):
    waste_listing = get_object_or_404(WasteListing, pk=pk, status='available')
    if request.method == 'POST':
        message = request.POST.get('message')
        subject = f"Inquiry about your waste listing: {waste_listing.title}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = waste_listing.user.email
        
        # Send email anonymously
        send_mail(
            subject,
            f"An anonymous user has sent you this message regarding your waste listing:\n\n{message}",
            from_email,
            [recipient_email],
            fail_silently=False,
        )
        messages.success(request, 'Your message has been sent anonymously!')
        return redirect('waste_detail', pk=pk)
    return redirect('waste_detail', pk=pk)

@login_required
def contact_product_owner(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message')
        subject = f"Inquiry about your product: {product.title}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_email = product.user.email
        
        send_mail(
            subject,
            f"An anonymous user has sent you this message regarding your product:\n\n{message}",
            from_email,
            [recipient_email],
            fail_silently=False,
        )
        messages.success(request, 'Your message has been sent anonymously!')
        return redirect('product_detail', pk=pk)
    return redirect('product_detail', pk=pk)

# marketplace/views.py
@login_required
def complete_waste_listing(request, pk):
    waste_listing = get_object_or_404(WasteListing, pk=pk, user=request.user)
    if waste_listing.status == 'available' or waste_listing.status == 'pending':
        waste_listing.mark_as_completed()
        messages.success(request, 'Waste listing marked as completed. You earned 10 Green Credits!')
    else:
        messages.error(request, 'This listing cannot be marked as completed.')
    return redirect('dashboard')
# Create your views here.

# Add Delete Waste Listing View
@login_required
def delete_waste_listing(request, pk):
    listing = get_object_or_404(WasteListing, pk=pk, user=request.user)  # Ensure only owner can delete
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Waste listing deleted successfully.')
        return redirect('dashboard')
    return redirect('waste_detail', pk=pk)  # Fallback for GET requests

# Add Delete Product View
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)  # Ensure only owner can delete
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('dashboard')
    return redirect('product_detail', pk=pk)  # Fallback for GET requests