from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from hospitals.models import Hospital, HospitalReview
from hospitals.forms import HospitalReviewForm
from requests_app.models import BedRequest
from bloodbanks.models import BloodBank

from django.db.models import Sum, Avg
from donors.models import Donor

def home(request):
    total_hospitals = Hospital.objects.filter(is_verified=True).count()
    total_bloodbanks = BloodBank.objects.filter(is_verified=True).count()
    total_donors = Donor.objects.count()
    
    bed_aggregate = Hospital.objects.filter(is_verified=True).aggregate(
        icu=Sum('icu_beds'),
        oxygen=Sum('oxygen_beds'),
        general=Sum('general_beds')
    )
    available_beds = (bed_aggregate['icu'] or 0) + (bed_aggregate['oxygen'] or 0) + (bed_aggregate['general'] or 0)

    context = {
        'total_hospitals': total_hospitals,
        'total_bloodbanks': total_bloodbanks,
        'total_donors': total_donors,
        'available_beds': available_beds,
    }
    return render(request, 'core/home.html', context)

def hospital_search(request):
    hospitals = Hospital.objects.filter(is_verified=True).annotate(avg_rating=Avg('reviews__rating'))
    
    city = request.GET.get('city')
    bed_type = request.GET.get('bed_type')
    
    if city:
        hospitals = hospitals.filter(city__icontains=city)
        
    if bed_type == 'icu':
        hospitals = hospitals.filter(icu_beds__gt=0)
    elif bed_type == 'oxygen':
        hospitals = hospitals.filter(oxygen_beds__gt=0)
    elif bed_type == 'general':
        hospitals = hospitals.filter(general_beds__gt=0)
        
    import json
    hospitals_data = []
    for h in hospitals:
        if h.latitude and h.longitude:
            hospitals_data.append({
                'id': h.id,
                'name': h.name,
                'lat': float(h.latitude),
                'lng': float(h.longitude),
                'beds': h.total_beds,
                'icu': h.icu_beds,
                'oxygen': h.oxygen_beds,
                'general': h.general_beds
            })
            
    return render(request, 'core/hospital_search.html', {
        'hospitals': hospitals,
        'city': city,
        'bed_type': bed_type,
        'hospitals_json': hospitals_data
    })

def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk, is_verified=True)
    reviews = hospital.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user is eligible to review
    can_review = False
    if request.user.is_authenticated:
        has_approved_request = BedRequest.objects.filter(
            hospital=hospital, 
            status='Completed' # Assuming 'Completed' or 'Approved'
        ).exists()
        
        has_reviewed = HospitalReview.objects.filter(hospital=hospital, user=request.user).exists()
        can_review = not has_reviewed

    if request.method == 'POST' and can_review:
        form = HospitalReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hospital = hospital
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('hospital_detail', pk=hospital.pk)
    else:
        form = HospitalReviewForm()
        
    hospital_data = None
    if hospital.latitude and hospital.longitude:
        hospital_data = {
            'id': hospital.id,
            'name': hospital.name,
            'lat': float(hospital.latitude),
            'lng': float(hospital.longitude),
            'beds': hospital.total_beds,
            'icu': hospital.icu_beds,
            'oxygen': hospital.oxygen_beds,
            'general': hospital.general_beds
        }
        
    return render(request, 'core/hospital_detail.html', {
        'hospital': hospital,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'form': form,
        'can_review': can_review,
        'hospital_json': hospital_data
    })

def bloodbank_search(request):
    bloodbanks = BloodBank.objects.filter(is_verified=True)
    
    city = request.GET.get('city')
    blood_group = request.GET.get('blood_group')
    
    if city:
        bloodbanks = bloodbanks.filter(city__icontains=city)
        
    if blood_group:
        if blood_group == 'A+': bloodbanks = bloodbanks.filter(a_pos__gt=0)
        elif blood_group == 'A-': bloodbanks = bloodbanks.filter(a_neg__gt=0)
        elif blood_group == 'B+': bloodbanks = bloodbanks.filter(b_pos__gt=0)
        elif blood_group == 'B-': bloodbanks = bloodbanks.filter(b_neg__gt=0)
        elif blood_group == 'AB+': bloodbanks = bloodbanks.filter(ab_pos__gt=0)
        elif blood_group == 'AB-': bloodbanks = bloodbanks.filter(ab_neg__gt=0)
        elif blood_group == 'O+': bloodbanks = bloodbanks.filter(o_pos__gt=0)
        elif blood_group == 'O-': bloodbanks = bloodbanks.filter(o_neg__gt=0)
        
    has_results = bloodbanks.exists()
    
    return render(request, 'core/bloodbank_search.html', {
        'bloodbanks': bloodbanks,
        'city': city,
        'blood_group': blood_group,
        'has_results': has_results,
        'searched': bool(city or blood_group)
    })

def sos_page(request):
    return render(request, 'core/sos.html')
