from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, IndustryApplication
from .forms import UserProfileForm, IndustryApplicationForm

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def apply_for_industry(request):
    # Check if user already has a pending or approved application
    existing_applications = IndustryApplication.objects.filter(
        user=request.user, 
        status__in=['pending', 'approved']
    )
    
    if existing_applications.exists() or request.user.profile.user_type == 'industry':
        messages.warning(request, 'You already have an industry application in process or are already registered as an industry.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = IndustryApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully and is under review.')
            return redirect('dashboard')
    else:
        form = IndustryApplicationForm()
    
    return render(request, 'accounts/industry_application.html', {'form': form})
# Create your views here.
def logout_user(request):
    logout(request)  # Logs out the user by clearing their session
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')