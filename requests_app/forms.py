from django import forms
from .models import BloodRequest, BedRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'blood_group', 'units_required', 'location_city', 'hospital_name', 'urgency']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'location_city': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
        }

class BedRequestForm(forms.ModelForm):
    class Meta:
        model = BedRequest
        fields = ['patient_name', 'contact_number', 'contact_email', 'age', 'gender', 'city', 'bed_type', 'emergency_notes', 'priority']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9876543210'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'For status updates'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'bed_type': forms.Select(attrs={'class': 'form-select'}),
            'emergency_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any specific medical conditions...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
