from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Donor
from .forms import DonorProfileForm
from requests_app.models import DonorResponse

@login_required
def donor_dashboard(request):
    if request.user.role != 'donor':
        return redirect('dashboard_redirect')
        
    donor, created = Donor.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_dashboard')
    else:
        form = DonorProfileForm(instance=donor)
        
    responses = DonorResponse.objects.filter(donor=donor).order_by('-created_at')
        
    return render(request, 'donors/dashboard.html', {
        'donor': donor,
        'form': form,
        'responses': responses,
    })
