from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BloodRequest, DonorResponse
from donors.models import Donor
from .forms import BloodRequestForm
from django.utils import timezone
from datetime import timedelta

@login_required
def create_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            
            # Matching Engine
            eligible_donors = Donor.objects.filter(
                blood_group=blood_request.blood_group,
                user__city__iexact=blood_request.location_city,
                is_available=True
            )
            
            for donor in eligible_donors:
                if donor.is_eligible:
                    # Create token
                    DonorResponse.objects.create(
                        blood_request=blood_request,
                        donor=donor,
                        status='Pending'
                    )
            
            return redirect('track_request', token=blood_request.tracking_token)
    else:
        form = BloodRequestForm()
        
    return render(request, 'requests_app/create_request.html', {'form': form})

def track_request(request, token):
    blood_request = get_object_or_404(BloodRequest, tracking_token=token)
    accepted_response = blood_request.responses.filter(status='Accepted').first()
    return render(request, 'requests_app/track_request.html', {
        'blood_request': blood_request,
        'accepted_response': accepted_response
    })

@login_required
def respond_request(request, token):
    response = get_object_or_404(DonorResponse, response_token=token)
    
    if request.user != response.donor.user:
        return redirect('/') # unauthorized
        
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if response.blood_request.status == 'Pending':
            if action == 'accept':
                response.status = 'Accepted'
                response.save()
                
                response.blood_request.status = 'Fulfilled'
                response.blood_request.save()
                
                # Update donor last donation date
                response.donor.last_donation_date = timezone.now().date()
                response.donor.save()
                
                # "First Donor Wins": Decline all other pending responses for this request
                DonorResponse.objects.filter(
                    blood_request=response.blood_request, 
                    status='Pending'
                ).exclude(id=response.id).update(status='Declined')
                
            elif action == 'decline':
                response.status = 'Declined'
                response.save()
                
            return redirect('donor_dashboard')
            
    return render(request, 'requests_app/respond_request.html', {'response': response})

from hospitals.models import Hospital
from .forms import BedRequestForm
from .models import BedRequest

def create_bed_request(request, hospital_id):
    selected_hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = BedRequestForm(request.POST)
        if form.is_valid():
            bed_request = form.save(commit=False)
            bed_request.hospital = selected_hospital
            bed_request.save()
            print(f"DEBUG: Saved BedRequest ID: {bed_request.id} for Hospital: {selected_hospital.name} (ID: {selected_hospital.id})")
            return redirect('track_bed_request', token=bed_request.tracking_token)
    else:
        initial_data = {'city': selected_hospital.city}
        bed_type = request.GET.get('bed_type')
        if bed_type:
            initial_data['bed_type'] = bed_type
            
        form = BedRequestForm(initial=initial_data)
        
    return render(request, 'requests_app/create_bed_request.html', {'form': form, 'hospital': selected_hospital})

def track_bed_request(request, token):
    bed_request = get_object_or_404(BedRequest, tracking_token=token)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'cancel' and bed_request.status in ['Pending', 'Under Review', 'Approved']:
            old_status = bed_request.status
            bed_request.status = 'Cancelled'
            bed_request.save()
            
            # If it was already approved, restore the bed
            if old_status == 'Approved':
                hosp = bed_request.hospital
                if bed_request.bed_type == 'ICU':
                    hosp.icu_beds += 1
                elif bed_request.bed_type == 'Oxygen':
                    hosp.oxygen_beds += 1
                elif bed_request.bed_type == 'General':
                    hosp.general_beds += 1
                hosp.save()
                
            return redirect('track_bed_request', token=token)
            
    return render(request, 'requests_app/track_bed_request.html', {'bed_request': bed_request})
