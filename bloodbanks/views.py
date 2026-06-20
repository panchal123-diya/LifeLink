from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BloodBank
from .forms import BloodBankProfileForm

@login_required
def bloodbank_dashboard(request):
    if request.user.role != 'bloodbank':
        return redirect('dashboard_redirect')
        
    bloodbank, created = BloodBank.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = BloodBankProfileForm(request.POST, instance=bloodbank)
        if form.is_valid():
            form.save()
            return redirect('bloodbank_dashboard')
    else:
        form = BloodBankProfileForm(instance=bloodbank)
        
    return render(request, 'bloodbanks/dashboard.html', {
        'bloodbank': bloodbank,
        'form': form,
    })
