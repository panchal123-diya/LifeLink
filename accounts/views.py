from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_redirect')
    else:
        form = AuthenticationForm()
        # Add bootstrap class to form
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')

@login_required
def dashboard_redirect(request):
    if request.user.role == 'hospital':
        return redirect('hospital_dashboard')
    elif request.user.role == 'bloodbank':
        return redirect('bloodbank_dashboard')
    elif request.user.role == 'donor':
        return redirect('donor_dashboard')
    else:
        return redirect('admin:index')

@login_required
def update_profile(request):
    from .forms import UserProfileForm
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = UserProfileForm(instance=request.user)
        
    return render(request, 'accounts/update_profile.html', {'form': form})
