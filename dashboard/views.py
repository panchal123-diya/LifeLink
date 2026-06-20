from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hospitals.models import Hospital
from bloodbanks.models import BloodBank
from donors.models import Donor
from requests_app.models import BloodRequest

@login_required
def analytics_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return render(request, 'base.html', {'content': 'Unauthorized access'})
        
    total_hospitals = Hospital.objects.count()
    total_bloodbanks = BloodBank.objects.count()
    total_donors = Donor.objects.count()
    
    total_requests = BloodRequest.objects.count()
    fulfilled_requests = BloodRequest.objects.filter(status='Fulfilled').count()
    critical_requests = BloodRequest.objects.filter(urgency='Critical').count()
    
    context = {
        'total_hospitals': total_hospitals,
        'total_bloodbanks': total_bloodbanks,
        'total_donors': total_donors,
        'total_requests': total_requests,
        'fulfilled_requests': fulfilled_requests,
        'critical_requests': critical_requests,
    }
    
    return render(request, 'dashboard/analytics.html', context)
