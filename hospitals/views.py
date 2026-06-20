from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hospital
from .forms import HospitalProfileForm
from requests_app.models import BedRequest
from django.utils import timezone

@login_required
def hospital_dashboard(request):
    if request.user.role != 'hospital':
        return redirect('dashboard_redirect')
        
    try:
        hospital = request.user.hospital
    except:
        hospital, created = Hospital.objects.get_or_create(user=request.user)
    
    print("Current Hospital:", hospital.id, hospital.name)

    all_requests = BedRequest.objects.all()

    for req in all_requests:
        print(
            f"Request ID={req.id}",
            f"Patient={req.patient_name}",
            f"Hospital={req.hospital.id if req.hospital else None}",
            f"Hospital Name={req.hospital.name if req.hospital else None}",
            f"Status={req.status}"
        )
    
    if request.method == 'POST':
        form = HospitalProfileForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_dashboard')
    else:
        form = HospitalProfileForm(instance=hospital)
        
    bed_requests = BedRequest.objects.filter(
        hospital=hospital
    ).order_by('-created_at')
    
    pending_count = BedRequest.objects.filter(
        hospital=hospital,
        status='Pending'
    ).count()
    
    stats = {
        'total': bed_requests.count(),
        'approved': bed_requests.filter(status='Approved').count(),
        'rejected': bed_requests.filter(status='Rejected').count(),
        'pending': pending_count,
    }

    return render(request, 'hospitals/dashboard.html', {
        'hospital': hospital,
        'form': form,
        'bed_requests': bed_requests,
        'stats': stats,
    })

@login_required
def respond_bed_request(request, request_id):
    if request.user.role != 'hospital':
        return redirect('/')
        
    bed_request = get_object_or_404(BedRequest, id=request_id, hospital__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if bed_request.status in ['Pending', 'Under Review']:
            if action == 'approve':
                bed_request.status = 'Approved'
                bed_request.approved_at = timezone.now()
                bed_request.save()
                
                # Reduce Available Bed Count
                hosp = bed_request.hospital
                if bed_request.bed_type == 'ICU' and hosp.icu_beds > 0:
                    hosp.icu_beds -= 1
                elif bed_request.bed_type == 'Oxygen' and hosp.oxygen_beds > 0:
                    hosp.oxygen_beds -= 1
                elif bed_request.bed_type == 'General' and hosp.general_beds > 0:
                    hosp.general_beds -= 1
                hosp.save()
                
            elif action == 'reject':
                bed_request.status = 'Rejected'
                bed_request.save()
                
        return redirect('hospital_dashboard')
